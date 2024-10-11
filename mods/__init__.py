# This file is placed in the Public Domain.
# pylint: disable=R,W0105,W0718


"command"


import importlib
import os


from nixt.object  import Obj, parse
from nixt.runtime import later, launch


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


def importdir(path, package="mods"):
    "import all files in directory."
    mods = []
    for fnm in os.listdir(path):
        if fnm.startswith("__"):
            continue
        if fnm.endswith("~"):
            continue
        pname = path.rsplit(os.sep, maxsplit=1)[-1]
        name = f"{pname}.{fnm[:-3]}"
        mods.append(importlib.import_module(name, package))
    return mods


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



importdir(os.path.dirname(__file__))
