# This file is placed in the Public Domain.[B
# pylint: disable=W0622


"find"


import time


from nixt.object  import format
from nixt.persist import find, fntime, laps, long, skel, types


from ..command  import Commands


def fnd(event):
    "locate objects."
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
        event.reply(f"{nmr} {format(obj)} {laps(time.time()-fntime(fnm))}")
        nmr += 1
    if not nmr:
        event.reply("no result")


Commands.add(fnd)