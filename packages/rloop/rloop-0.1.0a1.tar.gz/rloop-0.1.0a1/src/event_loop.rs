use std::{
    cmp::Ordering,
    collections::{BinaryHeap, VecDeque},
    mem,
    sync::{atomic, Arc, Mutex, RwLock},
    time::{Duration, Instant},
};

use anyhow::Result;
use dashmap::DashMap;
use mio::{Events, Interest, Poll, Token};
use pyo3::{prelude::*, types::PyDict};

use crate::handles::{CBHandle, TimerHandle};
use crate::io::Source;
use crate::py::{copy_context, weakset};

struct Timer {
    pub handle: Py<CBHandle>,
    when: u128,
}

impl PartialEq for Timer {
    fn eq(&self, _other: &Self) -> bool {
        false
    }
}

impl Eq for Timer {}

impl PartialOrd for Timer {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Timer {
    fn cmp(&self, other: &Self) -> Ordering {
        if self.when < other.when {
            return Ordering::Greater;
        }
        if self.when > other.when {
            return Ordering::Less;
        }
        Ordering::Equal
    }
}

struct IOHandleData {
    source: Source,
    interest: Interest,
    cbr: Option<Py<CBHandle>>,
    cbw: Option<Py<CBHandle>>,
}

#[pyclass(frozen, subclass)]
struct EventLoop {
    io: Arc<Mutex<Poll>>,
    handles_io: Arc<DashMap<Token, IOHandleData>>,
    handles_ready: Arc<Mutex<VecDeque<Py<CBHandle>>>>,
    handles_sched: Arc<Mutex<BinaryHeap<Timer>>>,
    epoch: Instant,
    closed: atomic::AtomicBool,
    stopping: atomic::AtomicBool,
    shutdown_called_asyncgens: atomic::AtomicBool,
    shutdown_called_executor: atomic::AtomicBool,
    task_factory: Arc<RwLock<PyObject>>,
    thread_id: atomic::AtomicI64,
    #[pyo3(get)]
    _asyncgens: PyObject,
    #[pyo3(get)]
    _base_ctx: PyObject,
    #[pyo3(get)]
    _default_executor: PyObject,
    #[pyo3(get)]
    _exception_handler: PyObject,
}

impl EventLoop {
    #[inline]
    fn _step(&self, py: Python) -> std::result::Result<(), std::io::Error> {
        let mut io_events = Events::with_capacity(128);
        let mut sched_time: Option<u64> = None;

        // compute poll timeout based on scheduled work
        // TODO: do we need the stopping one given we check for it in the outer loop?
        // if self._stopping.load(atomic::Ordering::Relaxed) {
        //     sched_time = Some(0);
        // } else {
        let has_ready_work = {
            let guard_cb = self.handles_ready.lock().unwrap();
            guard_cb.len() > 0
        };
        if has_ready_work {
            sched_time = Some(0);
        } else {
            let guard_sched = self.handles_sched.lock().unwrap();
            if let Some(timer) = guard_sched.peek() {
                let tick = Instant::now().duration_since(self.epoch).as_micros();
                if timer.when > tick {
                    let dt = ((timer.when - tick) / 1000) as u64;
                    sched_time = Some(dt);
                }
            }
            drop(guard_sched);
        }

        // I/O
        let poll_result = py.allow_threads(|| {
            let mut io = self.io.lock().unwrap();
            io.poll(&mut io_events, sched_time.map(Duration::from_millis))
        });
        let mut guard_cb = self.handles_ready.lock().unwrap();
        for event in &io_events {
            // NOTE: cancellation is not necessary as we have custom futures
            if let Some(handle) = self.handles_io.get(&event.token()) {
                if let Some(cbr) = &handle.cbr {
                    // if event.is_readable() && !cbr.get().cancelled.load(atomic::Ordering::Relaxed) {
                    //     guard_cb.push_back(cbr.clone_ref(py));
                    // }
                    if event.is_readable() {
                        guard_cb.push_back(cbr.clone_ref(py));
                    }
                }
                if let Some(cbw) = &handle.cbw {
                    // if event.is_writable() && !cbw.get().cancelled.load(atomic::Ordering::Relaxed) {
                    //     guard_cb.push_back(cbw.clone_ref(py));
                    // }
                    if event.is_writable() {
                        guard_cb.push_back(cbw.clone_ref(py));
                    }
                }
            }
        }

        // timers
        let mut guard_sched = self.handles_sched.lock().unwrap();
        if let Some(timer) = guard_sched.peek() {
            let tick = Instant::now().duration_since(self.epoch).as_micros();
            if timer.when <= tick {
                while let Some(timer) = guard_sched.peek() {
                    if timer.when > tick {
                        break;
                    }
                    guard_cb.push_back(guard_sched.pop().unwrap().handle);
                }
            }
        }
        drop(guard_sched);

        // callbacks
        let mut cb_handles = mem::replace(&mut *guard_cb, VecDeque::with_capacity(128));
        drop(guard_cb);
        while let Some(cb_handle) = cb_handles.pop_front() {
            // let handle = match cb_handle {
            //     Handle::Callback(ref v) => v.get(),
            //     Handle::IO(ref v) => v,
            //     // _ => unreachable!()
            // };
            let handle = cb_handle.get();
            if !handle.cancelled.load(atomic::Ordering::Relaxed) {
                if let Some((err, msg)) = handle.run(py) {
                    let err_ctx = PyDict::new_bound(py);
                    err_ctx.set_item(pyo3::intern!(py, "exception"), err).unwrap();
                    err_ctx.set_item(pyo3::intern!(py, "message"), msg).unwrap();
                    // err_ctx.set_item(pyo3::intern!(py, "handle"), cb_handle.clone_ref(py)).unwrap();

                    // TODO: how to call exception handler?
                }
            }
        }

        poll_result
    }

    #[inline]
    fn reader_rem(&self, token: Token) -> Result<bool> {
        if let Some((_, mut item)) = self.handles_io.remove(&token) {
            let guard_poll = self.io.lock().unwrap();
            match item.interest {
                Interest::READABLE => guard_poll.registry().deregister(&mut item.source)?,
                _ => {
                    let interest = Interest::WRITABLE;
                    guard_poll.registry().reregister(&mut item.source, token, interest)?;
                    self.handles_io.insert(
                        token,
                        IOHandleData {
                            source: item.source,
                            interest,
                            cbr: None,
                            cbw: item.cbw,
                        },
                    );
                }
            }
            return Ok(true);
        }
        Ok(false)
    }

    #[inline]
    fn writer_rem(&self, token: Token) -> Result<bool> {
        if let Some((_, mut item)) = self.handles_io.remove(&token) {
            let guard_poll = self.io.lock().unwrap();
            match item.interest {
                Interest::WRITABLE => guard_poll.registry().deregister(&mut item.source)?,
                _ => {
                    let interest = Interest::READABLE;
                    guard_poll.registry().reregister(&mut item.source, token, interest)?;
                    self.handles_io.insert(
                        token,
                        IOHandleData {
                            source: item.source,
                            interest,
                            cbr: item.cbr,
                            cbw: None,
                        },
                    );
                }
            }
            return Ok(true);
        }
        Ok(false)
    }
}

#[pymethods]
impl EventLoop {
    #[new]
    fn new(py: Python) -> PyResult<Self> {
        Ok(Self {
            io: Arc::new(Mutex::new(Poll::new()?)),
            handles_io: Arc::new(DashMap::with_capacity(128)),
            handles_ready: Arc::new(Mutex::new(VecDeque::with_capacity(128))),
            handles_sched: Arc::new(Mutex::new(BinaryHeap::with_capacity(32))),
            epoch: Instant::now(),
            closed: atomic::AtomicBool::new(false),
            stopping: atomic::AtomicBool::new(false),
            shutdown_called_asyncgens: atomic::AtomicBool::new(false),
            shutdown_called_executor: atomic::AtomicBool::new(false),
            task_factory: Arc::new(RwLock::new(py.None())),
            thread_id: atomic::AtomicI64::new(0),
            _asyncgens: weakset(py)?.unbind(),
            _base_ctx: copy_context(py)?.unbind(),
            _default_executor: py.None(),
            _exception_handler: py.None(),
        })
    }

    #[getter(_task_factory)]
    fn _get_task_factory(&self, py: Python) -> PyObject {
        self.task_factory.read().unwrap().clone_ref(py)
    }

    #[setter(_task_factory)]
    fn _set_task_factory(&self, factory: PyObject) {
        let mut guard = self.task_factory.write().unwrap();
        *guard = factory;
    }

    #[getter(_thread_id)]
    fn _get_thread_id(&self) -> i64 {
        self.thread_id.load(atomic::Ordering::Relaxed)
    }

    #[setter(_thread_id)]
    fn _set_thread_id(&self, val: i64) {
        self.thread_id.store(val, atomic::Ordering::Relaxed);
    }

    #[getter(_closed)]
    fn _get_closed(&self) -> bool {
        self.closed.load(atomic::Ordering::Relaxed)
    }

    #[setter(_closed)]
    fn _set_closed(&self, val: bool) {
        self.closed.store(val, atomic::Ordering::Relaxed);
    }

    #[getter(_stopping)]
    fn _get_stopping(&self) -> bool {
        self.stopping.load(atomic::Ordering::Relaxed)
    }

    #[setter(_stopping)]
    fn _set_stopping(&self, val: bool) {
        self.stopping.store(val, atomic::Ordering::Relaxed);
    }

    #[getter(_asyncgens_shutdown_called)]
    fn _get_asyncgens_shutdown_called(&self) -> bool {
        self.shutdown_called_asyncgens.load(atomic::Ordering::Relaxed)
    }

    #[setter(_asyncgens_shutdown_called)]
    fn _set_asyncgens_shutdown_called(&self, val: bool) {
        self.shutdown_called_asyncgens.store(val, atomic::Ordering::Relaxed);
    }

    #[getter(_executor_shutdown_called)]
    fn _get_executor_shutdown_called(&self) -> bool {
        self.shutdown_called_executor.load(atomic::Ordering::Relaxed)
    }

    #[setter(_executor_shutdown_called)]
    fn _set_executor_shutdown_called(&self, val: bool) {
        self.shutdown_called_executor.store(val, atomic::Ordering::Relaxed);
    }

    #[getter(_clock)]
    fn _get_clock(&self) -> u128 {
        Instant::now().duration_since(self.epoch).as_micros()
    }

    fn _call_soon(&self, py: Python, callback: PyObject, args: PyObject, context: PyObject) -> PyResult<Py<CBHandle>> {
        let handle = Py::new(py, CBHandle::new(callback, args, context))?;
        let mut guard = self.handles_ready.lock().unwrap();
        guard.push_back(handle.clone_ref(py));
        drop(guard);
        Ok(handle)
    }

    fn _call_later(
        &self,
        py: Python,
        delay: u64,
        callback: PyObject,
        args: PyObject,
        context: PyObject,
    ) -> PyResult<Py<TimerHandle>> {
        let when = Instant::now().duration_since(self.epoch).as_micros() + u128::from(delay);
        let handle = Py::new(py, CBHandle::new(callback, args, context))?;
        let thandle = Py::new(py, TimerHandle::new(handle.clone_ref(py), when))?;
        let mut guard = self.handles_sched.lock().unwrap();
        guard.push(Timer { handle, when });
        drop(guard);
        Ok(thandle)
    }

    fn _reader_add(
        &self,
        py: Python,
        fd: usize,
        callback: PyObject,
        args: PyObject,
        context: PyObject,
    ) -> PyResult<Py<CBHandle>> {
        let token = Token(fd);
        let handle = Py::new(py, CBHandle::new(callback, args, context))?;
        match self.handles_io.get_mut(&token) {
            Some(mut item) => {
                let interest = item.interest | Interest::READABLE;
                let guard_poll = self.io.lock().unwrap();
                guard_poll.registry().reregister(&mut item.source, token, interest)?;
                drop(guard_poll);
                item.interest = interest;
                item.cbr = Some(handle.clone_ref(py));
            }
            _ => {
                let mut source = Source::FD(fd.try_into()?);
                let interest = Interest::READABLE;
                let guard_poll = self.io.lock().unwrap();
                guard_poll.registry().register(&mut source, token, interest)?;
                drop(guard_poll);
                self.handles_io.insert(
                    token,
                    IOHandleData {
                        source,
                        interest,
                        cbr: Some(handle.clone_ref(py)),
                        cbw: None,
                    },
                );
            }
        }
        Ok(handle)
    }

    fn _reader_rem(&self, fd: usize) -> Result<bool> {
        let token = Token(fd);
        self.reader_rem(token)
    }

    fn _writer_add(
        &self,
        py: Python,
        fd: usize,
        callback: PyObject,
        args: PyObject,
        context: PyObject,
    ) -> PyResult<Py<CBHandle>> {
        let token = Token(fd);
        let handle = Py::new(py, CBHandle::new(callback, args, context))?;
        match self.handles_io.get_mut(&token) {
            Some(mut item) => {
                let interest = item.interest | Interest::WRITABLE;
                let guard_poll = self.io.lock().unwrap();
                guard_poll.registry().reregister(&mut item.source, token, interest)?;
                drop(guard_poll);
                item.interest = interest;
                item.cbw = Some(handle.clone_ref(py));
            }
            _ => {
                let mut source = Source::FD(fd.try_into()?);
                let interest = Interest::WRITABLE;
                let guard_poll = self.io.lock().unwrap();
                guard_poll.registry().register(&mut source, token, interest)?;
                drop(guard_poll);
                self.handles_io.insert(
                    token,
                    IOHandleData {
                        source,
                        interest,
                        cbr: None,
                        cbw: Some(handle.clone_ref(py)),
                    },
                );
            }
        }
        Ok(handle)
    }

    fn _writer_rem(&self, fd: usize) -> Result<bool> {
        let token = Token(fd);
        self.writer_rem(token)
    }

    fn _run(&self, py: Python) -> PyResult<()> {
        loop {
            if self.stopping.load(atomic::Ordering::Relaxed) {
                break;
            }
            if let Err(err) = self._step(py) {
                return Err(err.into());
            }
        }

        Ok(())
    }
}

pub(crate) fn init_pymodule(module: &Bound<PyModule>) -> PyResult<()> {
    module.add_class::<EventLoop>()?;

    Ok(())
}
