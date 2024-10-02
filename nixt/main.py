# This file is placed in the Public Domain.
# pylint: disable=R,W0105,C0413,W0611


"main"


import getpass
import inspect
import logging
import os
import pathlib
import pwd
import sys
import time
import threading
import _thread


from .command import Commands, command, scanner
from .object  import Obj, keys
from .runtime import Broker, Event, Reactor, later, launch


"defines"


NAME = __file__.rsplit(os.sep, maxsplit=2)[-2]
STARTTIME = time.time()
LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'warn': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

"config"


class Config(Obj):

     "Config"


"client"


class Client(Reactor):

    "Client"

    def __init__(self):
        Reactor.__init__(self)
        Broker.add(self)
        self.register("event", command)

    def display(self, evt):
        "show results into a channel."
        for txt in evt.result:
            self.say(evt.channel, txt)

    def say(self, _channel, txt):
        "echo on verbose."
        self.raw(txt)

    def raw(self, txt):
        "print to screen."
        raise NotImplementedError


"utilities"


def banner():
    "show banner."
    tme = time.ctime(time.time()).replace("  ", " ")
    logging.error(f"{NAME.upper()} since {tme}")


def enable(level):
    logging.basicConfig(stream=sys.stderr)
    format_plain = "%(message)s"
    datefmt = '%H:%M:%S'
    formatter = logging.Formatter(format_plain, datefmt=datefmt)
    lvl = LEVELS.get(level or "error")
    root = logging.getLogger()
    if root and root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
    ch = logging.StreamHandler()
    ch.setLevel(lvl)
    ch.setFormatter(formatter)
    root.addHandler(ch)


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
        for modname in modnames(pkg):
            modi = getattr(pkg, modname)
            if "init" not in dir(modi):
                continue
            thr = launch(modi.init)
            mods.append((modi, thr))
    return mods


def modnames(*args):
    "return module names."
    res = []
    for arg in args:
        res.extend([x for x in dir(arg) if not x.startswith("__")])
    return sorted(res)


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


def pidfile(filename):
    "write the pid to a file."
    if os.path.exists(filename):
        os.unlink(filename)
    path = pathlib.Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def privileges(username):
    "privileges."
    pwnam = pwd.getpwnam(username)
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


def wrap(func, outer):
    "reset console."
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        outer("")
    except Exception as ex:
        later(ex)


"interface"


def __dir__():
    return (
        'NAME',
        'STARTTIME',
        'Client',
        'Config',
        'banner',
        'enable',
        'forever',
        'init',
        'modnames',
        'parse',
        'pidfile',
        'privileges',
        'wrap'
    )
