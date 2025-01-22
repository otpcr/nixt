# This file is placed in the Public Domain.
# pylint: disable=C0116


"show list of commands"


from nixt.command import Commands


def cmd(event):
    event.reply(",".join(sorted(Commands.cmds.keys())))
