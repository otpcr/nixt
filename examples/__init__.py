# This file is placed in the Public Domain.
# pylint: disable=W0105,W0611,E0402
# ruff: noqa: F401


"interface"


import importlib
import os


from nixt.command import scan


DIR = os.path.dirname(__file__)
NAME = DIR.split(os.sep)[-1]

def importer(fqn):
    return importlib.import_module(fqn)
        

def importdir(pth):
    mods = []
    for fnm in os.listdir(pth):
        if not fnm.endswith(".py"):
             continue
        modname = fnm[:-3]
        mod = importer(f"{NAME}.{modname}")
        scan(mod)
        mods.append(mod)
    return mods


importdir(DIR)
