# This file is placed in the Public Domain.
# pylint: disable=R,W0105,W0212,W0718,E1102


"runtime"


import queue
import threading
import _thread


from .thread import launch
 

class Reactor:

    "Reactor"

    def __init__(self):
        self.cbs      = {}
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()

    def callback(self, evt):
        "call callback based on event type."
        func = self.cbs.get(evt.type, None)
        if func:
            evt._thr = launch(func, self, evt)

    def loop(self):
        "proces events until interrupted."
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def poll(self):
        "function to return event."
        return self.queue.get()

    def put(self, evt):
        "put event into the queue."
        self.queue.put_nowait(evt)

    def register(self, typ, cbs):
        "register callback for a type."
        self.cbs[typ] = cbs

    def start(self):
        "start the event loop."
        launch(self.loop)

    def stop(self):
        "stop the event loop."
        self.stopped.set()


class Client(Reactor):

    "Client"

    def display(self, evt):
        "show results into a channel."
        for txt in evt.result:
            self.say(evt.channel, txt)

    def say(self, _channel, txt):
        "echo on verbose."
        self.raw(txt)

    def raw(self, txt):
        "print to screen."
        raise NotImplementedError


class Event:

    "Event"

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
        "flag event as ready."
        self._ready.set()

    def reply(self, txt):
        "add text to the result."
        self.result.append(txt)

    def wait(self):
        "wait for results."
        self._ready.wait()
        if self._thr:
            self._thr.join()


def __dir__():
    return (
        'Client',
        'EVent',
        'Reactor'
    )
