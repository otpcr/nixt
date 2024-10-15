# This file is placed in the Public Domain.
# pylint: disable=C,R,W0105,W0718


"main program helpers"


import time
import _thread


from .object  import Obj, parse
from .runtime import later, launch


class Config(Obj):

    pass


class Commands:

    cmds = {}

    @staticmethod
    def add(func):
        Commands.cmds[func.__name__] = func


def command(bot, evt):
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


def forever():
    while True:
        try:
            time.sleep(1.0)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def init(*pkgs):
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
    try:
        result = txt.split(',')
    except (TypeError, ValueError):
        result = txt
    return [x for x in result if x]


def wrap(func):
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        pass
    except Exception as ex:
        later(ex)


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
