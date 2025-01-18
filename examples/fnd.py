# This file is placed in the Public Domain.
# pylint: disable=C0116,,W0105,W0622,E0402


"find"


import time


from nixt.objects import format
from nixt.persist import elapsed, find, fntime, long, skel, types


"commands"


def fnd(event):
    skel()
    if not event.rest:
        res = sorted([x.split('.')[-1].lower() for x in types()])
        if res:
            event.reply(",".join(res))
        return
    otype = event.args[0]
    clz = long(otype)
    nmr = 0
    for fnm, obj in find(clz, event.gets):
        event.reply(f"{nmr} {format(obj)} {elapsed(time.time()-fntime(fnm))}")
        nmr += 1
    if not nmr:
        event.reply("no result")
