# This file is placed in the Public Domain.


"uptime"


import time


STARTTIME = time.time()


from nixt.persist import laps


def upt(event):
    "show uptime"
    event.reply(laps(time.time()-STARTTIME))
