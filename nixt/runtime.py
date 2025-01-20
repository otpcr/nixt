# This file is placed in the Public Domain.


"runtime"


import queue
import threading
import time
import traceback
import _thread


class Reactor:

    """ Reactor """

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()
        self.stopped = threading.Event()

    def callback(self, evt):
        """ launch callback in thread."""
        func = self.cbs.get(evt.type, None)
        if func:
            evt.orig = repr(self)
            evt.thrs.append(launch(func, evt))

    def loop(self):
        """ reactor loop. """
        while not self.stopped.is_set():
            self.callback(self.poll())

    def poll(self):
        """ return event from queue. """
        return self.queue.get()

    def put(self, evt):
        """ put event in queue. """
        self.queue.put(evt)

    def raw(self, txt):
        """ echo text. """
        raise NotImplementedError("raw")

    def register(self, typ, cbs):
        """ register callback. """
        self.cbs[typ] = cbs

    def start(self):
        """ start reactor. """
        launch(self.loop)

    def stop(self):
        """ stop reactor. """
        self.stopped.set()

    def wait(self):
        """ wait for stop. """
        self.queue.join()
        self.stopped.wait()


class Thread(threading.Thread):

    """ Thread """

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
        """ return size of queue. """
        return self.queue.qsize()

    def join(self, timeout=None):
        """ join thread and return result. """
        super().join(timeout)
        return self.result

    def run(self):
        """ take job from queue and run it. """
        try:
            func, args = self.queue.get()
            self.result = func(*args)
        except (KeyboardInterrupt, EOFError, RuntimeError, SystemError):
            _thread.interrupt_main()
        except exceptions as ex:
            later(ex)
            try:
                args[0].ready()
            except (IndexError, AttributeError):
                pass


def launch(func, *args, **kwargs):
    """ run function in thread. """
    nme = kwargs.get("name", name(func))
    thread = Thread(func, nme, *args, **kwargs)
    thread.start()
    return thread


def name(obj):
    """ return name of an object. """
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


class Errors:

    """ Errors """

    errors = []

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    @staticmethod
    def format(exc):
        """ format exception. """
        return traceback.format_exception(
            type(exc),
            exc,
            exc.__traceback__
        )


def errors():
    """ yield printable error lines. """
    for err in Errors.errors:
        yield from err


def later(exc):
    """ defer exception. """
    excp = exc.with_traceback(exc.__traceback__)
    fmt = Errors.format(excp)
    if fmt not in Errors.errors:
        Errors.errors.append(fmt)


class Timer:

    """ Timer """

    def __init__(self, sleep, func, *args, thrname=None, **kwargs):
        self.args  = args
        self.func  = func
        self.kwargs = kwargs
        self.sleep = sleep
        self.name  = thrname or kwargs.get("name", name(func))
        self.state = {}
        self.timer = None

    def run(self):
        """ run timer at specific time. """
        self.state["latest"] = time.time()
        launch(self.func, *self.args)

    def start(self):
        """ start timer. """
        timer        = threading.Timer(self.sleep, self.func)
        timer.name   = self.name
        timer.sleep  = self.sleep
        timer.state  = self.state
        timer.func   = self.func
        timer.state["starttime"] = time.time()
        timer.state["latest"]    = time.time()
        timer.start()
        self.timer   = timer

    def stop(self):
        """ stop timer. """
        if self.timer:
            self.timer.cancel()


class Repeater(Timer):

    """ Repeater """

    def run(self):
        """ run at repeated intervals. """
        launch(self.start)
        super().run()


def forever():
    """ run forever. """
    while True:
        try:
            time.sleep(0.2)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


exceptions = (
    Exception,
    ArithmeticError,
    AssertionError,
    AttributeError,
    BufferError,
    ImportError,
    LookupError,
    MemoryError,
    NameError,
    OSError,
    ReferenceError,
    SyntaxError,
    SystemError
)


def __dir__():
    return (
        'Errors',
        'Reactor',
        'Repeater',
        'Thread',
        'Timer',
        'errors',
        'exceptions',
        'forever',
        'later',
        'launch',
        'name'
    )
