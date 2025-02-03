# This file is placed in the Public Domain.
# pylint: disable=C0116,E0402


"uptime"


import time


from ..clients import Config
from ..utility import elapsed


STARTTIME = time.time()


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))


def ver(event):
    event.reply(f"{Config.name.upper()} {Config.version}")
