# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0105,E0402


"clients"


import queue
import threading
import time


from .command import Default, command
from .runtime import Reactor, launch


"client"


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        self.register("command", command)
        Fleet.add(self)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def say(self, _channel, txt):
        self.raw(txt)


"event"


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready = threading.Event()
        self._thr   = None
        self.ctime  = time.time()
        self.result = []
        self.type   = "event"
        self.txt    = ""

    def display(self):
        for txt in self.result:
            Fleet.say(self.orig, self.channel, txt)

    def done(self):
        self.reply("ok")

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)

    def wait(self):
        self._ready.wait()
        if self._thr:
            self._thr.join()



"fleet"


class Fleet:

    bots = {}

    @staticmethod
    def add(bot):
        Fleet.bots[repr(bot)] = bot

    @staticmethod
    def announce(txt):
        for bot in Fleet.bots:
            bot.announce(txt)

    @staticmethod
    def get(orig):
        return Fleet.bots.get(orig, None)

    @staticmethod
    def say(orig, channel, txt):
        bot = Fleet.bots.get(orig, None)
        if bot:
            bot.say(channel, txt)


"output"


class Output:

    cache = {}

    def __init__(self):
        self.oqueue = queue.Queue()
        self.dostop = threading.Event()

    def dosay(self, channel, txt):
        raise NotImplementedError("dosay")

    def oput(self, channel, txt):
        self.oqueue.put((channel, txt))

    def output(self):
        while not self.dostop.is_set():
            (channel, txt) = self.oqueue.get()
            if channel is None and txt is None:
                self.oqueue.task_done()
                break
            self.dosay(channel, txt)
            self.oqueue.task_done()

    def start(self):
        launch(self.output)

    def stop(self):
        self.oqueue.join()
        self.dostop.set()
        self.oqueue.put((None, None))

    def wait(self):
        self.dostop.wait()


"interface"


def __dir__():
    return (
        'Client',
        'Fleet',
        'Output'
    )
