# This file is placed in the Public Domain.
# pylint: disable=C,W0718,E0402


"thread"


import queue
import threading
import time
import _thread


from .error import later


class Thread(threading.Thread):

    def __init__(self, func, thrname, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, thrname, (), {}, daemon=daemon)
        self.name = thrname or name(func)
        self.queue = queue.Queue()
        self.result = None
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


def __dir__():
    return (
        'Pool',
        'Thread',
        'Worker',
        'launch',
        'name'
    )
