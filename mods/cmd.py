# This file is placed in the Public Domain.
# pylint: disable=W0105


"list of commands"


from nixt.main   import Commands
from nixt.object import keys


def cmd(event):
    "list commands."
    event.reply(",".join(sorted(keys(Commands.cmds))))


"register"


def register():
    "register commands."
    Commands.add(cmd)
