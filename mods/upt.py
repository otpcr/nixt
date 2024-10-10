# This file is placed in the Public Domain.
# pylint: disable=W0105


"uptime"


import time


from nixt.command import Commands
from nixt.persist import laps
from nixt.runtime import STARTTIME


def register():
    "register commands."
    Commands.add(upt)


def upt(event):
    "show uptime"
    event.reply(laps(time.time()-STARTTIME))
