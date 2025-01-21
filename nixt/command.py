# This file is placed in the Public Domain.
# pylint: disable=W0105

"clients"


import inspect
import hashlib
import types


from .runtime import Config, Default, Fleet, Reactor, launch


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
        if modname and modname in spl(Config.dis):
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


MD5 = {
    "cmd": "a8bf5c9c5019c6e90b557e07f7d7f186",
    "err": "6929af2979007bfbeb8007492360317e",
    "fnd": "768f01a0ca8d94fdb50d94a9b1133f45",
    "irc": "d60772ae6562284ffc91aed7136b46fe",
    "log": "1ef7b4cd8268401bff6a5500e2d0ca8f",
    "mod": "905102ea6cd9a3a6e2a0f0bd3d73ebe5",
    "req": "464fb82d2ec152bfcffbab99fb6de3af",
    "rss": "dbf3724b8a2f043ad89e4dc8adee5e49",
    "thr": "73d28b9bb90152b5ab234ef73a7d0676",
    "upt": "563823b2bd6ba4b68c79a9ca687c513d"
}


def __dir__():
    return (
        'MD5',
        'Commands',
        'command',
        'md5sum',
        'parse',
        'scan',
        'spl'
    )
