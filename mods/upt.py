# This file is placed in the Public Domain.


"uptime"


import time


from nixt.main    import STARTTIME, Commands
from nixt.persist import laps


def register():
    "register commands."
    Commands.add(upt)


def upt(event):
    "show uptime"
    event.reply(laps(time.time()-STARTTIME))
