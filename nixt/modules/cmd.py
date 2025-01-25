# This file is placed in the Public Domain.
# pylint: disable=C0116,E0402


"show list of commands"


from ..command import NAMES, Config, spl


def cmd(event):
    event.reply(",".join(sorted([
                                 x for x in NAMES.keys()
                                 if x not in spl(Config.dis)
                                ]
                               )))
