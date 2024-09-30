# This file is placed in the Public Domain.


"commands."


from ..        import keys
from ..command import Commands


def cmd(event):
    "list commands."
    event.reply(",".join(sorted(keys(Commands.cmds))))


Commands.add(cmd)
