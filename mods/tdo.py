# This file is placed in the Public Domain.
# pylint: disable=R,W0105


"todo list"


import time


from nixt.main    import Commands
from nixt.object  import Object
from nixt.persist import find, fntime, laps, sync


class Todo(Object):

    "Todo"

    def __init__(self):
        Object.__init__(self)
        self.txt = ''


def dne(event):
    "flag todo as done."
    if not event.args:
        event.reply("dne <txt>")
        return
    selector = {'txt': event.args[0]}
    nmr = 0
    for fnm, obj in find('todo', selector):
        nmr += 1
        obj.__deleted__ = True
        sync(obj, fnm)
        event.reply('ok')
        break
    if not nmr:
        event.reply("nothing todo")


def tdo(event):
    "add todo."
    if not event.rest:
        nmr = 0
        for fnm, obj in find('todo'):
            lap = laps(time.time()-fntime(fnm))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply("no todo")
        return
    obj = Todo()
    obj.txt = event.rest
    sync(obj)
    event.reply('ok')


"register"


def register():
    "register commands."
    Commands.add(dne)
    Commands.add(tdo)
