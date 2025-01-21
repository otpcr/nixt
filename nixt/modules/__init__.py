# This file is placed in the Public Domain.


"modules"


import importlib
import os


from ..command import md5sum
from ..runtime import Config


DIR  = os.path.dirname(__file__)
MODS = []
NAME = ".".join(DIR.rsplit(os.sep, maxsplit=2)[-2:])


def importer(fqn, modname):
    """ import full qualified name. """
    return importlib.import_module(fqn, modname)


def importdir(pth, check=Config.md5):
    """ import a complete directory. """
    for fnm in os.listdir(pth):
        if fnm.startswith("__"):
            continue
        if not fnm.endswith(".py"):
            continue
        modname = fnm[:-3]
        if check:
            skip = True
            fnm = f"{pth}/{fnm}"
            with open(fnm, "r", encoding="utf-8") as file:
                data = file.read()
                if MD5.get(modname) == md5sum(data):
                    skip = False
            if skip:
                continue
        importer(f"{NAME}.{modname}", f"{NAME}")
        MODS.append(modname)

"md5sums"

MD5 = {
    "cmd": "a8bf5c9c5019c6e90b557e07f7d7f186",
    "err": "6929af2979007bfbeb8007492360317e",
    "fnd": "a078262c5bccf0cc96e269ee3cdfb904",
    "irc": "50974365f7ca588dd309b7aa730132ab",
    "log": "db6fa3608e4c9664af163edda07cdca6",
    "mod": "905102ea6cd9a3a6e2a0f0bd3d73ebe5",
    "req": "464fb82d2ec152bfcffbab99fb6de3af",
    "rss": "6aefa61277016449f099ee0b61cf72fe",
    "thr": "475be28c992348f2faaccb4a5b01724a",
    "upt": "9cacb986f2e83a8b772fe639a4fa5c80"
}


importdir(DIR)


def __dir__():
    return MODS
