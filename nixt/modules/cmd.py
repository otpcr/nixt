# This file is placed in the Public Domain.
# pylint: disable=C,E0402


"commands"


from ..command import Command


def cmd(event):
    event.reply(",".join(sorted(Command.cmds.keys())))
