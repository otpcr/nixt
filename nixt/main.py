# This file is placed in the Public Domain.


"main"


import time
import _thread


from .runtime import launch


NAME = __file__.rsplit("/", maxsplit=2)[-2]
STARTTIME = time.time()


def boot(*pkgs, mods=None):
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
        for modname in dir(pkg):
            if modname.startswith("__"):
                continue
            modi = getattr(pkg, modname)
            if "init" not in dir(modi):
                continue
            thr = launch(modi.init)
            mods.append((modi, thr))
    return mods


def spl(txt):
    "split comma separated string into a list."
    try:
        result = txt.split(',')
    except (TypeError, ValueError):
        result = txt
    return [x for x in result if x]


def wrap(func):
    "reset console."
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        pass
    except Exception as ex:
        later(ex)


def __dir__():
    return (
        'boot',
        'forever',
        'init',
        'spl',
        'wrap'
    )