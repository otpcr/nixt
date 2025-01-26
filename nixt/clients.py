# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,W0105,W0212,W0613,W0718,E0402


"clients"


import queue
import threading
import time


from .runtime import Reactor, launch


"output"


def debug(txt):
    if "v" in Config.opts:
        output(txt)


def output(txt):
    # output here
    print(txt)


"default"


class Default:

    def __contains__(self, key):
        return key in dir(self)

    def __getattr__(self, key):
        return self.__dict__.get(key, "")

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


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
        Output.start()

    def raw(self, txt):
        raise NotImplementedError("raw")


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
        for bot in Fleet.bots.values():
            bot.announce(txt)

    @staticmethod
    def display(evt):
        for text in evt.result:
            Fleet.say(evt.orig, evt.channel, text)

    @staticmethod
    def first():
        bots =  list(Fleet.bots.values())
        res = None
        if bots:
            res = bots[0]
        return res

    @staticmethod
    def get(orig):
        return Fleet.bots.get(orig, None)

    @staticmethod
    def say(orig, channel, txt):
        bot = Fleet.get(orig)
        if bot:
            bot.say(channel, txt)


"output"


class Output:

    queue   = queue.Queue()
    running = threading.Event()

    @staticmethod
    def loop():
        Output.running.set()
        while Output.running.is_set():
            evt = Output.queue.get()
            if evt is None:
                break
            Fleet.display(evt)

    @staticmethod
    def put(evt):
        if not Output.running.is_set():
            Fleet.display(evt)
        Output.queue.put_nowait(evt)

    @staticmethod
    def start():
        if not Output.running.is_set():
            Output.running.set()
            launch(Output.loop)

    @staticmethod
    def stop():
        Output.running.clear()
        Output.queue.put(None)


"interface"


def __dir__():
    return (
        'Default',
        'Client',
        'Event',
        'Fleet'
    )
