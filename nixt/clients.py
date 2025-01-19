# This file is placed in the Public Domain.
# pylint: disable=W0105,E0402


""" clients """


import queue
import threading
import time


from .command import Default, command
from .runtime import Reactor, launch


"client"


class Client(Reactor):

    """ Client """

    def __init__(self):
        Reactor.__init__(self)
        self.register("command", command)
        Fleet.add(self)

    def raw(self, txt):
        """ echo text. """
        raise NotImplementedError("raw")

    def say(self, _channel, txt):
        """ relay to raw. """
        self.raw(txt)


"event"


class Event(Default):

    """ Event """

    def __init__(self):
        Default.__init__(self)
        self._ready = threading.Event()
        self.thrs   = []
        self.ctime  = time.time()
        self.result = []
        self.type   = "event"
        self.txt    = ""

    def display(self):
        """ display result."""
        for txt in self.result:
            Fleet.say(self.orig, self.channel, txt)

    def done(self):
        """ signal done."""
        self.reply("ok")

    def ready(self):
        """ signal ready."""
        self._ready.set()

    def reply(self, txt):
        """ add text to result. """
        self.result.append(txt)

    def wait(self):
        """ wait for finished. """
        self._ready.wait()
        for thr in  self.thrs:
            thr.join()


"fleet"


class Fleet:

    """ Fleet. """

    bots = {}

    @staticmethod
    def add(bot):
        """ add to fleet."""
        Fleet.bots[repr(bot)] = bot

    @staticmethod
    def announce(txt):
        """ announce on fleet."""
        for bot in Fleet.bots:
            bot.announce(txt)

    @staticmethod
    def get(orig):
        """get by origin."""
        return Fleet.bots.get(orig, None)

    @staticmethod
    def say(orig, channel, txt):
        """ say text on channel on specific bot."""
        bot = Fleet.bots.get(orig, None)
        if bot:
            bot.say(channel, txt)


"output"


class Output:

    """ Output """

    cache = {}

    def __init__(self):
        self.oqueue = queue.Queue()
        self.dostop = threading.Event()

    def dosay(self, channel, txt):
        """ inherit this. """
        raise NotImplementedError("dosay")

    def oput(self, channel, txt):
        """ put output to outqueue. """
        self.oqueue.put((channel, txt))

    def output(self):
        """ output loop. """
        while not self.dostop.is_set():
            (channel, txt) = self.oqueue.get()
            if channel is None and txt is None:
                self.oqueue.task_done()
                break
            self.dosay(channel, txt)
            self.oqueue.task_done()

    def start(self):
        """ start loop."""
        launch(self.output)

    def stop(self):
        """ stop loop."""
        self.oqueue.join()
        self.dostop.set()
        self.oqueue.put((None, None))

    def wait(self):
        """ wait for stop."""
        self.dostop.wait()


"interface"


def __dir__():
    return (
        'Client',
        'Event',
        'Fleet',
        'Output'
    )
