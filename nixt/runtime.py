# This file is placed in the Public Domain.
# pylint: disable=C,R,W0212,W0718


"runtime"


import queue
import threading
import time
import traceback
import types
import _thread


class Errors:

    errors = []


def fmat(exc):
    return traceback.format_exception(
                               type(exc),
                               exc,
                               exc.__traceback__
                              )


def later(exc):
    excp = exc.with_traceback(exc.__traceback__)
    fmt = fmat(excp)
    if fmt not in Errors.errors:
        Errors.errors.append(fmt)


class Thread(threading.Thread):

    def __init__(self, func, thrname, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, thrname, (), {}, daemon=daemon)
        self.name      = thrname
        self.queue     = queue.Queue()
        self.result    = None
        self.starttime = time.time()
        self.queue.put_nowait((func, args))

    def __contains__(self, key):
        return key in self.__dict__

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def size(self):
        return self.queue.qsize()

    def join(self, timeout=None):
        super().join(timeout)
        return self.result

    def run(self):
        try:
            func, args = self.queue.get()
            self.result = func(*args)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()
        except Exception as ex:
            later(ex)


def launch(func, *args, **kwargs):
    name = kwargs.get("name", named(func))
    thread = Thread(func, name, *args, **kwargs)
    thread.start()
    return thread


def named(obj):
    if isinstance(obj, types.ModuleType):
        return obj.__name__
    typ = type(obj)
    if '__builtins__' in dir(typ):
        return obj.__name__
    if '__self__' in dir(obj):
        return f'{obj.__self__.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj) and '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj):
        return f"{obj.__class__.__module__}.{obj.__class__.__name__}"
    if '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    return None


class Reactor:

    def __init__(self):
        self.cbs      = {}
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()

    def callback(self, evt):
        func = self.cbs.get(evt.type, None)
        if func:
            evt._thr = launch(func, self, evt)

    def loop(self):
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def poll(self):
        return self.queue.get()

    def put(self, evt):
        self.queue.put_nowait(evt)

    def register(self, typ, cbs):
        self.cbs[typ] = cbs

    def start(self):
        launch(self.loop)

    def stop(self):
        self.stopped.set()


class Client(Reactor):

    def display(self, evt):
        for txt in evt.result:
            self.say(evt.channel, txt)

    def say(self, _channel, txt):
        self.raw(txt)

    def raw(self, txt):
        raise NotImplementedError


class Event:

    def __init__(self):
        self._ready  = threading.Event()
        self._thr    = None
        self.channel = ""
        self.orig    = ""
        self.result  = []
        self.txt     = ""
        self.type    = "event"

    def __getattr__(self, key):
        return self.__dict__.get(key, "")

    def __str__(self):
        return str(self.__dict__)

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)

    def wait(self):
        self._ready.wait()
        if self._thr:
            self._thr.join()


class Timer:

    def __init__(self, sleep, func, *args, thrname=None, **kwargs):
        self.args  = args
        self.func  = func
        self.kwargs = kwargs
        self.sleep = sleep
        self.name  = thrname or kwargs.get("name", named(func))
        self.state = {}
        self.timer = None

    def run(self):
        self.state["latest"] = time.time()
        launch(self.func, *self.args)

    def start(self):
        timer = threading.Timer(self.sleep, self.run)
        timer.name   = self.name
        timer.sleep  = self.sleep
        timer.state  = self.state
        timer.func   = self.func
        timer.state["starttime"] = time.time()
        timer.state["latest"]    = time.time()
        timer.start()
        self.timer   = timer

    def stop(self):
        if self.timer:
            self.timer.cancel()


class Repeater(Timer):

    def run(self):
        launch(self.start)
        super().run()


def forever():
    while True:
        try:
            time.sleep(1.0)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def wrap(func):
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        pass
    except Exception as ex:
        later(ex)


def __dir__():
    return (
        'Client',
        'Event',
        'Reactor',
        'Errors',
        'Repeater',
        'Thread',
        'Timer',
        'forever',
        'format',
        'later',
        'launch',
        'init',
        'named',
        'wrap'
    )
