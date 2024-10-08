# This file is placed in the Public Domain.
# pylint: disable=W0105,W0719


"debug"


from nixt.command import Commands


def register():
    "register commands."
    Commands.add(dbg)


def dbg(event):
    "raise exception."
    raise Exception("yo!")
