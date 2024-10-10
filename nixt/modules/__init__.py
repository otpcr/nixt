# This file is placed in the Public Domain.
# pylint: disable=R,W0105,W0718


"command"


from ..object  import Obj, parse
from ..runtime import later


class Commands:

    "Commands"

    cmds = {}

    @staticmethod
    def add(func):
        "add command."
        Commands.cmds[func.__name__] = func


def command(bot, evt):
    "check for and run a command."
    parse(evt, evt.txt)
    if "ident" in dir(bot):
        evt.orig = bot.ident
    func = Commands.cmds.get(evt.cmd, None)
    if func:
        try:
            func(evt)
            bot.display(evt)
        except Exception as ex:
            later(ex)
    evt.ready()


"utilities"


def scan(*pkgs, mods=None):
    "run the init function in modules."
    wanted = spl(mods or "")
    for pkg in pkgs:
        for mod in dir(pkg):
            if wanted and mod not in wanted:
                continue
            if mod.startswith("__"):
                continue
            modi = getattr(pkg, mod)
            if "register" not in dir(modi):
                continue
            modi.register()


def spl(txt):
    "split comma separated string into a list."
    try:
        result = txt.split(',')
    except (TypeError, ValueError):
        result = txt
    return [x for x in result if x]


def __dir__():
    return (
        'Commands',
        'command',
        'parse',
        'scan',
        'spl'
    )
