# This file is placed in the Public Domain.


"show errors"


from nixt.runtime import Errors


from ..command  import Commands


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


Commands.add(err)
