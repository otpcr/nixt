# This file is placed in the Public Domain.


"user commands"


import inspect
import types


from .objects import Object
from .runtime import later, launch


class Default(Object):

    "Default"

    def __contains__(self, key):
        return key in dir(self)

    def __getattr__(self, key):
        return self.__dict__.get(key, "")

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):

        return len(self.__dict__)


class Config(Default):

    "Config"

    name = Default.__module__.split(".", maxsplit=1)[0]


class Commands:

    "Commands"

    cmds = {}

    @staticmethod
    def add(func):
        "add command."
        Commands.cmds[func.__name__] = func

    @staticmethod
    def scan(mod):
        "scan modules for commands."
        for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmdz.__code__.co_varnames:
                Commands.add(cmdz)


def command(evt):
    "check for and execute command."
    parse(evt)
    func = Commands.cmds.get(evt.cmd, None)
    if func:
        try:
            func(evt)
            evt.display()
        except Exception as ex:
            later(ex)
    evt.ready()


"utilities"


def modloop(*pkgs, disable=""):
    "return modules names in a directory."
    for pkg in pkgs:
        for modname in dir(pkg):
            if modname in spl(disable):
                continue
            if modname.startswith("__"):
                continue
            yield getattr(pkg, modname)


def parse(obj, txt=None):
    "parse an object for commands." 
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
            if key == "mod":
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


def scan(*pkgs, init=False, disable=""):
    "scan all modules in a package."
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
    "comma seprated value string."
    try:
        result = txt.split(',')
    except (TypeError, ValueError):
        result = txt
    return [x for x in result if x]


def __dir__():
    return (
        'Commands',
        'Config',
        'Default',
        'command',
        'parse',
        'scan'
    )
