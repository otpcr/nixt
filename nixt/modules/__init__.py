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
            print(fnm)
            with open(fnm, "r", encoding="utf-8") as file:
                data = file.read()
                if MD5.get(modname) == md5sum(data):
                    skip = False
            if skip:
                print(f"skipped {fnm}")
                continue
        importer(f"{NAME}.{modname}", f"{NAME}")
        MODS.append(modname)


MD5 = {
    "cmd": "a8bf5c9c5019c6e90b557e07f7d7f186",
    "err": "6929af2979007bfbeb8007492360317e",
    "fnd": "2595f54340dab9e37cdaa9e19f30863c",
    "irc": "c7d2bf0885b1a092431d66c17d6ece74",
    "log": "180f8a4cd6e85200764b5459d1131aea",
    "mod": "905102ea6cd9a3a6e2a0f0bd3d73ebe5",
    "req": "464fb82d2ec152bfcffbab99fb6de3af",
    "rss": "6988be7b7c826fcf21e136360c9bf2e4",
    "thr": "3e6798073a40e18fb48f5a7fc326ee25",
    "upt": "3dd0694099265f5850ac7720d9631df9"
}


importdir(DIR)


def __dir__():
    return MODS
