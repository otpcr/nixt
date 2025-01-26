# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,W0105,W0212,W0613,W0718,E0402


"runtime"


import importlib
import queue
import threading
import time
import traceback
import _thread


"defines"


STARTTIME = time.time()


"reactor"


class Reactor:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()
        self.stopped = threading.Event()

    def callback(self, evt):
        func = self.cbs.get(evt.type, None)
        if func:
            try:
                evt._thr = launch(func, evt)
            except Exception as ex:
                later(ex)
                evt.ready()

    def loop(self):
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                if evt is None:
                    break
                evt.orig = repr(self)
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                if "ready" in dir(evt):
                    evt.ready()
                _thread.interrupt_main()

    def poll(self):
        return self.queue.get()

    def put(self, evt):
        self.queue.put(evt)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def register(self, typ, cbs):
        self.cbs[typ] = cbs

    def start(self):
        launch(self.loop)

    def stop(self):
        self.stopped.set()
        self.queue.put(None)

    def wait(self):
        self.queue.join()
        self.stopped.wait()


"thread"


class Thread(threading.Thread):

    def __init__(self, func, thrname, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self.name = thrname
        self.queue = queue.Queue()
        self.starttime = time.time()
        self.stopped = threading.Event()
        self.queue.put((func, args))

    def run(self):
        func, args = self.queue.get()
        try:
            func(*args)
        except Exception as ex:
            later(ex)
            try:
                args[0].ready()
            except (IndexError, AttributeError):
                pass


def launch(func, *args, **kwargs):
    nme = kwargs.get("name", name(func))
    thread = Thread(func, nme, *args, **kwargs)
    thread.start()
    return thread


def name(obj):
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


"timers"


class Timer:

    def __init__(self, sleep, func, *args, thrname=None, **kwargs):
        self.args   = args
        self.func   = func
        self.kwargs = kwargs
        self.sleep  = sleep
        self.name   = thrname or kwargs.get("name", name(func))
        self.state  = {}
        self.timer  = None

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


"errors"


class Errors:

    errors = []

    @staticmethod
    def format(exc):
        return traceback.format_exception(
            type(exc),
            exc,
            exc.__traceback__
        )


def errors():
    for err in Errors.errors:
        yield from err


def later(exc):
    excp = exc.with_traceback(exc.__traceback__)
    fmt = Errors.format(excp)
    if fmt not in Errors.errors:
        Errors.errors.append(fmt)


"table"


class Table:

    mods = {}

    @staticmethod
    def add(mod):
        Table.mods[mod.__name__] = mod

    @staticmethod
    def get(name):
        return Table.mods.get(name, None)

    @staticmethod
    def inits(names, wait=False):
        name = Errors.__module__.split(".", maxsplit=1)[0]
        mods = []
        pname = f"{name}.modules"
        for name in spl(names):
            mname = f"{pname}.{name}"
            mod = Table.load(mname)
            thr = launch(mod.init)
            mods.append((mod, thr))
        if wait:
            for _, thr in mods:
                thr.join()
        return mods

    @staticmethod
    def load(name):
        pname = Errors.__module__
        mname  = f"{pname}/{name}"
        mod = Table.mods.get(mname)
        if not mod:
            Table.mods[name] = mod = importlib.import_module(name, name)
        return mod

    @staticmethod
    def scan(pkg, mods=""):
        for name in dir(pkg):
            if mods and name not in spl(mods):
                continue
            mod = Table.load(f'{pname}.{name}')
            Commands.scan(mod)
        if not Table.mods:
            Table.scan(pkg)


"cache"


class Cache:

    objs = {}

    @staticmethod
    def add(path, obj):
        Cache.objs[path] = obj

    @staticmethod
    def get(path):
        return Cache.objs.get(path, None)

    @staticmethod
    def typed(matcher):
        for key in Cache.objs:
            if matcher not in key:
                continue
            yield Cache.objs.get(key)


"utilities"


def spl(txt):
    try:
        result = txt.split(',')
    except (TypeError, ValueError):
        result = txt
    return [x for x in result if x]



"interface"


def __dir__():
    return (
        'STARTTIME',
        'Cache',
        'Errors',
        'Reactor',
        'Repeater',
        'Table',
        'Thread',
        'Timer',
        'errors',
        'later',
        'launch',
        'name'
    )
