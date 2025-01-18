# This file is placed in the Public Domain.
# pylint: disable=C0116,W0105,W0611,E0402
# ruff: noqa: F401


"interface"


import hashlib
import importlib
import os


from nixt.command import MD5


DIR  = os.path.dirname(__file__)
NAME = ".".join(DIR.rsplit(os.sep, maxsplit=2)[-2:])


def importer(fqn):
    return importlib.import_module(fqn)


def md5sum(txt):
    return hashlib.md5(txt.encode("utf-8")).hexdigest()


def importdir(pth):
    mods = []
    for fnm in os.listdir(pth):
        if fnm.startswith("__"):
            continue
        if not fnm.endswith(".py"):
            continue
        skip = True
        with open(f"{pth}/{fnm}", "r", encoding="utf-8").read() as data:
            if MD5.get(fnm) == md5sum(data):
                skip = False
        if skip:
            continue
        modname = fnm[:-3]
        mod = importer(f"{NAME}.{modname}")
        mods.append(mod)
    return mods


importdir(DIR)
