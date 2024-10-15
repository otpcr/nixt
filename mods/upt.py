# This file is placed in the Public Domain.
# pylint: disable=W0105


"uptime"


import time


from nixt.main    import Commands
from nixt.persist import laps


STARTTIME = time.time()


def upt(event):
    event.reply(laps(time.time()-STARTTIME))


def register():
    Commands.add(upt)
