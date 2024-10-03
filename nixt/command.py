#!/usr/bin/env python3
# This file is placed in the Public Domain.
# pylint: disable=R,W0105,C0413,W0611,W0718


"command"


import inspect


from .object  import Obj
from .persist import pidfile, pidname
from .runtime import later


class Commands:

    "Commands"

    cmds = {}

    @staticmethod
    def add(func):
        "add command."
        Commands.cmds[func.__name__] = func


class Config(Obj):

    "Config"


def command(bot, evt):
    "check for and run a command."
    parse(evt, evt.txt)
    evt.orig = repr(bot)
    func = Commands.cmds.get(evt.cmd, None)
    if func:
        try:
            func(evt)
            bot.display(evt)
        except Exception as ex:
            later(ex)
    evt.ready()


def parse(obj, txt=None):
    "parse a string for a command."
    if txt is None:
        txt = ""
    args = []
    obj.args    = []
    obj.cmd     = ""
    obj.gets    = Obj()
    obj.hasmods = False
    obj.index   = None
    obj.mod     = ""
    obj.opts    = ""
    obj.result  = []
    obj.sets    = Obj()
    obj.txt     = txt or ""
    obj.otxt    = obj.txt
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            val = getattr(obj.gets, key, None)
            if val:
                value = val + "," + value
                setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                obj.hasmods = True
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            setattr(obj.sets, key, value)
            continue
        _nr += 1
        if _nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt  = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd or ""
    return obj


def scan(mod):
    "scan module for commands."
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in cmd.__code__.co_varnames:
            Commands.add(cmd)


def scanner(*pkgs):
    "scan modules for commands and classes"
    mds = []
    for pkg in pkgs:
        for modname in dir(pkg):
            module = getattr(pkg, modname, None)
            if not module:
                continue
            scan(module)
            mds.append(module)
    return mds


def __dir__():
    return (
        'Commands',
        'Config',
        'command',
        'parse',
        'pidfile',
        'pidname',
        'scan',
        'scanner'
    )
