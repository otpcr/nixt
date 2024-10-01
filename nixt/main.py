# This file is placed in the Public Domain.
# pylint: disable=R,W0105,W0718,E1102


"utilities for main"


import os
import pathlib
import pwd
import time
import _thread


from .runtime import debug, later, launch


NAME      = __file__.rsplit("/", maxsplit=2)[-2]
STARTTIME = time.time()


"utilities"


def banner():
    "show banner."
    tme = time.ctime(time.time()).replace("  ", " ")
    debug(f"{NAME.upper()} since {tme}")


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
        'Logging',
        'debug',
        'forever',
        'init',
        'modnames',
        'pidfile',
        'privileges'
    )
