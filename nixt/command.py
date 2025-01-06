# This file is placed in the Public Domain.


"commands"


import inspect
import types
import _thread


from .error import later
from .parse import parse


commandlock = _thread.allocate_lock()


class Command:

    cmds = {}

    @staticmethod
    def add(func):
        Command.cmds[func.__name__] = func

    @staticmethod
    def scan(mod):
        for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmdz.__code__.co_varnames:
                Command.add(cmdz)


def command(bot, evt):
    with commandlock:
        parse(evt, evt.txt)
        if "ident" in dir(bot):
            evt.orig = bot.ident
        func = Command.cmds.get(evt.cmd, None)
        if func:
            try:
                func(evt)
                bot.display(evt)
            except Exception as ex:
                later(ex)
        evt.ready()


def modloop(*pkgs, disable=""):
    for pkg in pkgs:
        for modname in dir(pkg):
            if modname in spl(disable):
                continue
            if modname.startswith("__"):
                continue
            yield getattr(pkg, modname)


def scan(*pkgs, init=False, disable=""):
    result = []
    for mod in modloop(*pkgs, disable=disable):
        if type(mod) is not types.ModuleType:
            continue
        Command.scan(mod)
        thr = None
        if init and "init" in dir(mod):
            thr = launch(mod.init)
        result.append((mod, thr))
    return result


def spl(txt):
    try:
        result = txt.split(',')
    except (TypeError, ValueError):
        result = txt
    return [x for x in result if x]
