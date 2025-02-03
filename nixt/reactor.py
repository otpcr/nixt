# This file is placed in the Public Domain.


"reactor"


import queue
import threading
import time
import _thread


from .default import Default
from .excepts import later
from .threads import launch


cblock = threading.RLock()
lock   = threading.RLock()


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready = threading.Event()
        self._thr   = None
        self.ctime  = time.time()
        self.result = {}
        self.type   = "event"
        self.txt    = ""

    def display(self) -> None:
        Fleet.display(self)

    def done(self) -> None:
        self.reply("ok")

    def ready(self) -> None:
        self._ready.set()

    def reply(self, txt) -> None:
        self.result[time.time()] = txt

    def wait(self) -> None:
        self._ready.wait()
        if self._thr:
            self._thr.join()


class Reactor:

    def __init__(self):
        self.cbs     = {}
        self.queue   = queue.Queue()
        self.ready   = threading.Event()
        self.stopped = threading.Event()

    def callback(self, evt) -> None:
        with cblock:
            func = self.cbs.get(evt.type, None)
            if func:
                try:
                    evt._thr = launch(func, evt, name=evt.cmd or evt.txt)
                except Exception as ex:
                    later(ex)
                    evt.ready()

    def loop(self) -> None:
        evt = None
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                if evt is None:
                    break
                evt.orig = repr(self)
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                if evt:
                    evt.ready()
                _thread.interrupt_main()
        self.ready.set()

    def poll(self) -> Event:
        return self.queue.get()

    def put(self, evt) -> None:
        self.queue.put(evt)

    def raw(self, txt) -> None:
        raise NotImplementedError("raw")

    def register(self, typ, cbs) -> None:
        self.cbs[typ] = cbs

    def start(self) -> None:
        self.stopped.clear()
        self.ready.clear()
        launch(self.loop)

    def stop(self) -> None:
        self.stopped.set()
        self.queue.put(None)

    def wait(self) -> None:
        self.ready.wait()


class Fleet:

    bots = {}

    @staticmethod
    def add(bot) -> None:
        Fleet.bots[repr(bot)] = bot

    @staticmethod
    def announce(txt) -> None:
        for bot in Fleet.bots.values():
            bot.announce(txt)

    @staticmethod
    def display(evt) -> None:
        with lock:
            for tme in sorted(evt.result):
                text = evt.result[tme]
                Fleet.say(evt.orig, evt.channel, text)
            evt.ready()

    @staticmethod
    def first() -> None:
        bots =  list(Fleet.bots.values())
        res = None
        if bots:
            res = bots[0]
        return res

    @staticmethod
    def get(orig) -> None:
        return Fleet.bots.get(orig, None)

    @staticmethod
    def say(orig, channel, txt) -> None:
        bot = Fleet.get(orig)
        if bot:
            bot.say(channel, txt)

    @staticmethod
    def wait():
        for bot in Fleet.bots.values():
            if "wait" in dir(bot):
                bot.wait()


def __dir__():
    return (
        'Event',
        'Fleet',
        'Reactor'
    )
