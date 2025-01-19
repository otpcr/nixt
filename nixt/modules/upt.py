# This file is placed in the Public Domain.
# pylint: disable=E0402


"uptime"


import time


from ..locator import elapsed


STARTTIME = time.time()


def upt(event):
    """ show uptime. """
    event.reply(elapsed(time.time()-STARTTIME))
