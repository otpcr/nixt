# This file is placed in the Public Domain.
# pylint: disable=C


"uptime"


import time


from nixt.persist import laps
from nixt.runtime import Commands


STARTTIME = time.time()


def upt(event):
    event.reply(laps(time.time()-STARTTIME))


def register():
    Commands.add(upt)
