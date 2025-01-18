# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,W0105,E0402


"user commands"


import inspect
import types


from .objects import Object
from .runtime import launch


"commands"


class Commands:

    cmds = {}

    @staticmethod
    def add(func):
        "add command."
        Commands.cmds[func.__name__] = func

    @staticmethod
    def scan(mod):
        for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmdz.__code__.co_varnames:
                Commands.add(cmdz)


def command(evt):
    parse(evt)
    func = Commands.cmds.get(evt.cmd, None)
    if func:
        func(evt)
        evt.display()
    evt.ready()


"default"


class Default(Object):

    def __contains__(self, key):
        return key in dir(self)

    def __getattr__(self, key):
        return self.__dict__.get(key, "")

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)


"config"


class Config(Default):

    name = Default.__module__.split(".", maxsplit=1)[0]


"utilitites"


def modloop(*pkgs, disable=""):
    for pkg in pkgs:
        for modname in dir(pkg):
            if modname in spl(disable):
                continue
            if modname.startswith("__"):
                continue
            yield getattr(pkg, modname)


def parse(obj, txt=None):
    if txt is None:
        if "txt" in dir(obj):
            txt = obj.txt
        else:
            txt = ""
    args = []
    obj.args    = []
    obj.cmd     = ""
    obj.gets    = Default()
    obj.index   = None
    obj.mod     = ""
    obj.opts    = ""
    obj.result  = []
    obj.sets    = Default()
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
            setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
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


def scan(*pkgs, init=False, disable=""):
    result = []
    for mod in modloop(*pkgs, disable=disable):
        if not isinstance(mod, types.ModuleType):
            continue
        Commands.scan(mod)
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


"data"


MD5 = {
    "cmd": "9114fb0c1a3d103044dd9bda61de0ec6",
    "err": "e37bb27c6cad4b1f888f8e096ad4ba4c",
    "fnd": "b76855ea818b0983d09f5ab63a88e0d7",
    "irc": "a03f529855b2b70ea8523b948e13b515",
    "log": "ae5a6d7d08e04de524af9e8b23be0536",
    "mod": "abb31624685eaa65b5d9d2aa93024347",
    "opm": "17fb3a704f1fb9c30c6c8d25b74aa81f",
    "req": "faddd66da68fbcb979b25297113916c6",
    "rss": "46a0c57432069b0b197a2f9486a755fd",
    "thr": "c51caeb8ca19375444654f3cf02b7c2c",
    "upt": "9d4b125b198161a247d1c128f67519c2"
}


"interface"


def __dir__():
    return (
        'MD%',
        'Commands',
        'Config',
        'Default',
        'Event',
        'command',
        'parse',
        'scan',
        'spl'
    )
