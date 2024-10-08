# This file is placed in the Public Domain.


"modules"


import importlib
import os


def importdir(path, package="mods"):
    "import all files in directory."
    mods = []
    for fnm in os.listdir(path):
        if fnm.startswith("__"):
            continue
        if fnm.endswith("~"):
            continue
        pname = path.rsplit(os.sep, maxsplit=1)[-1]
        name = f"{pname}.{fnm[:-3]}"
        mods.append(importlib.import_module(name, package))
    return mods


importdir(os.path.dirname(__file__))
           