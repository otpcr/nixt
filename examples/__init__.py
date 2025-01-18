# This file is placed in the Public Domain.
# pylint: disable=W0105,W0611,E0402
# ruff: noqa: F401


"interface"


import hashlib
import importlib
import os


DIR  = os.path.dirname(__file__)
ENABLE = ["irc.py",]
NAME = ".".join(DIR.rsplit(os.sep, maxsplit=1)[-1:])
MD5  = {
    "req.py": "faddd66da68fbcb979b25297113916c6",
    "rss.py": "46a0c57432069b0b197a2f9486a755fd",
    "log.py": "ae5a6d7d08e04de524af9e8b23be0536",
    "opm.py": "17fb3a704f1fb9c30c6c8d25b74aa81f",
    "fnd.py": "b76855ea818b0983d09f5ab63a88e0d7",
    "irc.py": "a03f529855b2b70ea8523b948e13b515"
}


def importer(fqn):
    return importlib.import_module(fqn)


def md5sum(txt):
    return hashlib.md5(txt.encode("utf-8")).hexdigest()
        

def importdir(pth):
    mods = []
    for fnm in os.listdir(pth):
        if fnm not in ENABLE:
            continue
        data = open(f"{pth}/{fnm}", "r").read()
        if MD5.get(fnm, "") != md5sum(data):
             continue
        modname = fnm[:-3]
        mod = importer(f"{NAME}.{modname}")
        mods.append(mod)
    return mods


importdir(DIR)
