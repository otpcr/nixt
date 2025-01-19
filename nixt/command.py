# This file is placed in the Public Domain.
# pylint: disable=W0105,E0402


"commands"


import inspect
import hashlib
import types


from .objects import Object
from .runtime import launch


"default"


class Default(Object):

    """ Default """

    default = ""

    def __contains__(self, key):
        return key in dir(self)

    def __getattr__(self, key):
        return self.__dict__.get(key, self.default)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    @staticmethod
    def getdefault():
        """ return default. """
        return Default.default

    @staticmethod
    def setdefault(default):
        """ set default. """
        Default.default = default


"config"


class Config(Default):

    """ Config. """

    dis  = ""
    mods = ""
    name = Default.__module__.split(".", maxsplit=1)[0]


"commands"


class Commands:

    """ Commands """

    cmds = {}

    @staticmethod
    def add(func):
        """ add command. """
        Commands.cmds[func.__name__] = func

    @staticmethod
    def scan(mod):
        """ scan module for commands. """
        for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmdz.__code__.co_varnames:
                Commands.add(cmdz)


def command(evt):
    """ command callback. """
    parse(evt)
    func = Commands.cmds.get(evt.cmd, None)
    if func:
        func(evt)
        evt.display()
    evt.ready()


"utilities"


def md5sum(txt):
    """ create md5 sum of text. """
    return hashlib.md5(txt.encode("utf-8")).hexdigest()


def modloop(*pkgs, disable=""):
    """ yield modules in package. """
    for pkg in pkgs:
        for modname in dir(pkg):
            if modname in spl(disable):
                continue
            if modname.startswith("__"):
                continue
            yield getattr(pkg, modname)


def parse(obj, txt=None):
    """ parse text into object. """
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
    """ scan package for command and init scripts. """
    result = []
    for mod in modloop(*pkgs, disable=disable):
        modname = mod.__name__.split(".")[-1]
        if Config.mods and modname not in spl(Config.mods):
            continue
        if not isinstance(mod, types.ModuleType):
            continue
        Commands.scan(mod)
        thr = None
        if init and "init" in dir(mod):
            thr = launch(mod.init)
        result.append((mod, thr))
    return result


def spl(txt):
    """ comma seperated string. """
    try:
        result = txt.split(',')
    except (TypeError, ValueError):
        result = txt
    return [x for x in result if x]


"data"


MD5 = {
    "cmd": "e78043b056cf96aaf89f1c7120c1cd2d",
    "err": "5be6a5e9979ce54ee6732042e2f94ca0",
    "fnd": "01bf50246b2359fb50b2525be1534224",
    "irc": "cad25097e75b162e1fac703d48d3b97f",
    "log": "8eb40f6b95daf57780d28d7f1b7a80c5",
    "mod": "abb31624685eaa65b5d9d2aa93024347",
    "opm": "cc5f3d72512e0cc07c0211ad4db173b8",
    "req": "faddd66da68fbcb979b25297113916c6",
    "rss": "abe8a2dae8de3827ba67ecb60f730676",
    "thr": "e7c0a98c0eec0d2c8186ea23651ae7e2",
    "upt": "22016f78b86dd0a4f4fa25b2de2ff76b"
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
        'md5sum',
        'parse',
        'scan',
        'spl'
    )
