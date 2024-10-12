# This file is placed in the Public Domain.
# pylint: disable=W0105


"show errors"


from nixt.main    import Commands
from nixt.runtime import Errors


def err(event):
    "show errors."
    nmr = 0
    for exc in Errors.errors:
        for line in exc:
            event.reply(line.strip())
        nmr += 1
    if not nmr:
        event.reply("no errors")
        return
    event.reply(f"found {nmr} errors.")


"register"


def register():
    "register commands."
    Commands.add(err)
