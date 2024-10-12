# This file is placed in the Public Domain.
# pylint: disable=R0903,W0105,W0718


"main program helpers"


import time
import _thread


from .object  import Obj, parse
from .runtime import later, launch


"defines"


class Config(Obj):

    "Config"


NAME = __file__.rsplit("/", maxsplit=2)[-2]
STARTTIME = time.time()


"commands"


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


def forever():
    "it doesn't stop, until ctrl-c"
    while True:
        try:
            time.sleep(1.0)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def init(*pkgs):
    "run the init function in modules."
    mods = []
    for pkg in pkgs:
        for modname in dir(pkg):
            if modname.startswith("__"):
                continue
            modi = getattr(pkg, modname)
            if "init" not in dir(modi):
                continue
            thr = launch(modi.init)
            mods.append((modi, thr))
    return mods


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


def wrap(func):
    "reset console."
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        pass
    except Exception as ex:
        later(ex)


"interface"


def __dir__():
    return (
        'Commands',
        'Config',
        'forever',
        'init',
        'scan',
        'spl',
        'wrap'
    )
