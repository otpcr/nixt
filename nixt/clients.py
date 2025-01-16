# This file is placed in the Public Domain.


"clients"


import queue
import threading
import time


from .command import Default, command
from .runtime import Reactor, launch


class Config(Default):

    "Config"

    name = Default.__module__.split(".")[0]


    def size(self):
        "return size of config."
        return len(self.__dict__)

    def saved(self):
        "bogus"
        return True


class Client(Reactor):

    "Client"

    def __init__(self):
        Reactor.__init__(self)
        self.register("command", command)
        Fleet.add(self)

    def raw(self, txt):
        "echo text to screen."
        raise NotImplementedError("raw")

    def say(self, channel, txt):
        "say something on a channel."
        raise NotImplementedError("say")


class Event(Default):

    "Event"

    def __init__(self):
        Default.__init__(self)
        self._ready = threading.Event()
        self._thr   = None
        self.ctime  = time.time()
        self.result = []
        self.type   = "event"
        self.txt    = ""

    def display(self):
        "display on origin bot."
        for txt in self.result:
            Fleet.say(self.orig, self.channel, txt)

    def done(self):
        "signal completion."
        self.reply("ok")

    def ready(self):
        "signal ready."
        self._ready.set()

    def reply(self, txt):
        "add to result."
        self.result.append(txt)

    def wait(self):
        "wait for ready and join thread."
        self._ready.wait()
        if self._thr:
            self._thr.join()


class Fleet:

    "Fleet"

    bots = {}

    @staticmethod
    def add(bot):
        "add bot to fleet."
        Fleet.bots[repr(bot)] = bot

    @staticmethod
    def announce(txt):
        "annouce text on bots."
        for bot in Fleet.bots:
            bot.announce(txt)

    @staticmethod
    def get(orig):
        "return bot by origin."
        return Fleet.bots.get(orig, None)

    @staticmethod
    def say(orig, channel, txt):
        "say something on specific bot."
        bot = Fleet.bots.get(orig, None)
        if bot:
            bot.say(channel, txt)


class Output:

    "Output"

    cache = {}

    def __init__(self):
        self.oqueue = queue.Queue()
        self.dostop = threading.Event()

    def dosay(self, channel, txt):
        "say something on remote bot."
        raise NotImplementedError("dosay")

    def oput(self, channel, txt):
        "put text to output queue."
        self.oqueue.put((channel, txt))

    def output(self):
        "loop to ourpur text from queue."
        while not self.dostop.is_set():
            (channel, txt) = self.oqueue.get()
            if channel is None and txt is None:
                self.oqueue.task_done()
                break
            self.dosay(channel, txt)
            self.oqueue.task_done()

    def start(self):
        "start output loop."
        launch(self.output)

    def stop(self):
        "stop output loop."
        self.oqueue.join()
        self.dostop.set()
        self.oqueue.put((None, None))

    def wait(self):
        "wait for loop to quit."
        self.dostop.wait()


def __dir__():
    return (
        'Client',
        'Config',
        'Fleet',
        'Output'
    )
