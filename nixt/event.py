# This file is placed in the Public Domain.
# pylint: disable=C,E0402


"event"


import datetime
import os
import threading
import time


from .object import fqn


p = os.path.join


class Event:

    def __init__(self):
        self._id    = ident(self)
        self._ready = threading.Event()
        self._thr   = None
        self.result = []
        self.type   = "event"
        self.txt    = ""

    def __getattr__(self, key):
        return self.__dict__.get(key, "")

    def __str__(self):
        return str(self.__dict__)

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)

    def wait(self):
        self._ready.wait()
        if self._thr:
            self._thr.join()


def ident(obj):
    return p(fqn(obj), *str(datetime.datetime.now()).split())


def idtime(daystr):
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    return timed


def __dir__():
    return (
        'Event',
        'fqn',
        'ident',
        'idtime'
    )
