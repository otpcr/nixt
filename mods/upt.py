# This file is placed in the Public Domain.
# pylint: disable=W0105


"uptime"


import time


from nixt.persist import laps
from nixt.runtime import STARTTIME


from .command import Commands


def register():
    "register commands."
    Commands.add(upt)


def upt(event):
    "show uptime"
    event.reply(laps(time.time()-STARTTIME))
