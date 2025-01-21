# This file is placed in the Public Domain.


"log text"


import time


from ..base import Object
from ..disk import ident, store, write
from ..find import elapsed, find, fntime


class Log(Object):

    """ Log """

    def __init__(self):
        super().__init__()
        self.txt = ''

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


def log(event):
    """ log some text. """
    if not event.rest:
        nmr = 0
        for fnm, obj in find('log'):
            lap = elapsed(time.time() - fntime(fnm))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply('no log')
        return
    obj = Log()
    obj.txt = event.rest
    write(obj, store(ident(obj)))
    event.done()
