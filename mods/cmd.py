# This file is placed in the Public Domain.
# pylint: disable=C,W0105


"list of commands"


from nixt.object  import keys
from nixt.runtime import Commands


def cmd(event):
    event.reply(",".join(sorted(keys(Commands.cmds))))


def register():
    Commands.add(cmd)
