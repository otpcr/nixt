# This file is placed in the Public Domain.


"uptime"


import time


from ..clients import Config
from ..runtime import STARTTIME
from ..utility import elapsed


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))


def ver(event):
    event.reply(f"{Config.name.upper()} {Config.version}")
