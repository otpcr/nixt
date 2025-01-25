# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0912,W0105,E0402


"user commands"


import importlib
import inspect
import os
import types


from .clients import Default, Output
from .runtime import later, launch


try:
    from .lookups import NAMES
except Exception as ex:
    later(ex)
    NAMES = {}


"defines"


def debug(txt):
    if "v" in Config.opts:
        output(txt)


def output(txt):
    # output here
    print(txt)


"config"


class Config(Default):

    dis  = "mbx,mdl,rst,slg,tmr,udp,wsd"
    name = Default.__module__.rsplit(".", maxsplit=2)[-2]
    opts = Default()


"commands"


class Commands:

    cmds = {}
    names = NAMES

    @staticmethod
    def add(func, mod=None):
        Commands.cmds[func.__name__] = func
        if mod:
            Commands.names[func.__name__] = mod.__name__

    @staticmethod
    def get(cmd):
        return Commands.cmds.get(cmd, None)

    @staticmethod
    def getname(cmd):
        return Commands.names.get(cmd, None)

    @staticmethod
    def scan(mod):
        if mod.__name__.split(".")[-1] in spl(Config.dis):
            return
        for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmdz.__code__.co_varnames:
                Commands.add(cmdz, mod)
        return


"table"


class Table:

    mods = {}

    @staticmethod
    def add(mod):
        Table.mods[mod.__name__] = mod

    @staticmethod
    def get(name):
        return Table.mods.get(name, None)

    @staticmethod
    def load(name):
        Table.mods[name] = mod = importlib.import_module(name, 'nixt.modules')
        Commands.scan(mod)
        return mod

    @staticmethod
    def scan(pkg, pname=None):
        if pname is None:
            pname = "nixt.modules" 
        for name in dir(pkg):
            if name in spl(Config.dis):
                 continue
            mod = Table.load(f"nixt.modules.{name}")
        if not Table.mods:
            scan(pkg)


"callbacks"


def command(evt):
    parse(evt)
    func = Commands.get(evt.cmd)
    if not func:
        mname = Commands.getname(evt.cmd)
        if not mname:
            evt.ready()
            return
        if mname.split(".")[-1] in spl(Config.dis):
            evt.ready()
            return
        debug(f"autoload {mname}")
        Table.load(mname)
        func = Commands.get(evt.cmd)
    if func:
        func(evt)
        Output.put(evt)
    evt.ready()


"Scanner"


def modloop(*pkgs, disable=""):
    for pkg in pkgs:
        print(pkg)
        if pkg is None:
            continue
        for name in  [x[:-3] for x in os.listdir(os.path.dirname(pkg.__file__))
                      if not x.startswith("__")]:
            yield Table.load(f"nixt.modules.{name}")


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


"utilities"


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


def spl(txt):
    try:
        result = txt.split(',')
    except (TypeError, ValueError):
        result = txt
    return [x for x in result if x]


"interface"


def __dir__():
    return (
        'Commands',
        'command',
        'cmd',
        'parse',
        'scan'
    )
