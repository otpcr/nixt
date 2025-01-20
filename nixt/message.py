# This file is placed in the Public Domain.


"message"


import threading
import time


from .caching import Fleet


class Message:

    """ Message """

    def __init__(self):
        self._ready = threading.Event()
        self.thrs   = []
        self.ctime  = time.time()
        self.result = []
        self.type   = "event"
        self.txt    = ""

    def __getattr__(self, key):
        return self.__dict__.get(key, "")

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


def __dir__():
    return (
        'Message',
    )
