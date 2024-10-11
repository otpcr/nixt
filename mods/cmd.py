# This file is placed in the Public Domain.
# pylint: disable=W0105


"list of commands"


from nixt.object  import keys


from . import Commands


def register():
    "register commands."
    Commands.add(cmd)


def cmd(event):
    "list commands."
    event.reply(",".join(sorted(keys(Commands.cmds))))
