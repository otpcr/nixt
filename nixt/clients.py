# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,W0105,W0212,W0613,W0718,E0402


"clients"


import queue
import threading
import time


from .runtime import Default, Event, Fleet, Reactor, launch


"locks"


lock = threading.RLock()


"output"


def debug(txt):
    if "v" in Config.opts:
        output(txt)


def output(txt):
    # output here
    pass


"config"


class Config(Default):

    init = "irc,rss"
    name = Default.__module__.rsplit(".", maxsplit=2)[-2]
    opts = Default()


"clients"


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        Fleet.add(self)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def say(self, channel, txt):
        self.raw(txt)


class Buffered(Client):

    def __init__(self):
        Client.__init__(self)
        Output.__init__(self)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def start(self):
        Output.start(self)
        Client.start(self)

    def stop(self):
        Client.stop(self)
        Output.stop(self)

    def wait(self):
        Client.wait(self)
        Output.wait(self)


"output"


class Output:

    def __init__(self):
        self.oqueue   = queue.Queue()
        self.running = threading.Event()

    @staticmethod
    def loop():
        self.running.set()
        while self.running.is_set():
            evt = self.oqueue.get()
            if evt is None:
                self.oqueue.task_done()
                break
            Fleet.display(evt)
            self.oqueue.task_done()

    @staticmethod
    def oput(self,evt):
        if not Output.running.is_set():
            Fleet.display(evt)
        self.oqueue.put(evt)

    @staticmethod
    def start(self):
        if not self.running.is_set():
            self.running.set()
            launch(self.loop)

    @staticmethod
    def stop(self):
        self.running.clear()
        self.oqueue.put(None)

    @staticmethod
    def wait(self):
        self.oqueue.join()


"interface"


def __dir__():
    return (
        'Default',
        'Client',
        'Event',
        'Fleet'
    )
