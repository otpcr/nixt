# This file is placed in the Public Domain.


"show uptime/version"


import time


from ..clients import STARTTIME, Config
from ..utility import elapsed


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))


def ver(event):
    event.reply(f"{Config.name.upper()} {Config.version}")
