# This file is placed in the Public Domain.
# pylint: disable=W0105


"uptime"


import time


from nixt.main    import STARTTIME, Commands
from nixt.persist import laps


def upt(event):
    "show uptime"
    event.reply(laps(time.time()-STARTTIME))


"register"


def register():
    "register commands."
    Commands.add(upt)
