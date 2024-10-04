# This file is placed in the Public Domain.


"uptime"


import time


from nixt.persist import laps


from ..command  import STARTTIME, Commands


def upt(event):
    "show uptime"
    event.reply(laps(time.time()-STARTTIME))


Commands.add(upt)
