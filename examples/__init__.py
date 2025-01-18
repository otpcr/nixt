# This file is placed in the Public Domain.
# pylint: disable=C0116,W0105,W0611,E0402
# ruff: noqa: F401


"interface"


import hashlib
import importlib
import os


from nixt.command import MD5


DIR  = os.path.dirname(__file__)
MODS = []
NAME = ".".join(DIR.rsplit(os.sep, maxsplit=1)[-1:])


def importer(fqn, modname):
    return importlib.import_module(fqn, modname)


def md5sum(txt):
    return hashlib.md5(txt.encode("utf-8")).hexdigest()


def importdir(pth):
    mods = []
    for fnm in os.listdir(pth):
        if fnm.startswith("__"):
            continue
        if not fnm.endswith(".py"):
            continue
        modname = fnm[:-3]
        data = open(f"{pth}/{fnm}", "r", encoding="utf-8").read()
        if MD5.get(modname) != md5sum(data):
            continue
        mod = importer(f"{NAME}.{modname}", f"{NAME}")
        MODS.append(modname)


importdir(DIR)

def __dir__():
    return MODS
