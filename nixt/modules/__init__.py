# This file is placed in the Public Domain.
# pylint: disable=W0105,W0611,E0402
# ruff: noqa: F401


"interface"


import hashlib
import importlib
import os


from nixt.command import scan


DIR  = os.path.dirname(__file__)
NAME = ".".join(DIR.rsplit(os.sep, maxsplit=2)[-2:])
MD5  = {
    "mod.py": "abb31624685eaa65b5d9d2aa93024347",
    "upt.py": "22016f78b86dd0a4f4fa25b2de2ff76b",
    "cmd.py": "e78043b056cf96aaf89f1c7120c1cd2d",
    "thr.py": "e7c0a98c0eec0d2c8186ea23651ae7e2",
    "err.py": "5be6a5e9979ce54ee6732042e2f94ca0"
}


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
        data = open(f"{pth}/{fnm}", "r").read()
        if MD5.get(fnm) != md5sum(data):
             continue
        modname = fnm[:-3]
        mod = importer(f"{NAME}.{modname}")
        mods.append(mod)
    return mods


importdir(DIR)
