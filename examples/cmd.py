# This file is placed in the Public Domain.
# pylint: disable=C0116,W0105,E0402


"show list of commands"


from nixt.command import Commands


"commands"


def cmd(event):
    event.reply(",".join(sorted(Commands.cmds.keys())))
