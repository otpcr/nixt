# This file is placed in the Public Domain.
# pylint: disable=C0116,W0105,E0402


"""uptime"""


import time


from nixt.persist import elapsed


STARTTIME = time.time()


def upt(event):
    """ show uptime. """
    event.reply(elapsed(time.time()-STARTTIME))
