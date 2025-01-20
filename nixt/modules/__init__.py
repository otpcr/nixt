# This file is placed in the Public Domain.


""" modules """


import importlib
import os


from ..command import MD5, md5sum


DIR  = os.path.dirname(__file__)
MODS = []
NAME = ".".join(DIR.rsplit(os.sep, maxsplit=2)[-2:])


def importer(fqn, modname):
    """ import full qualified name. """
    return importlib.import_module(fqn, modname)


def importdir(pth, check=False):
    """ import a complete directory. """
    for fnm in os.listdir(pth):
        if fnm.startswith("__"):
            continue
        if not fnm.endswith(".py"):
            continue
        modname = fnm[:-3]
        if check:
            skip = True
            with open(f"{pth}/{fnm}", "r", encoding="utf-8") as file:
                data = file.read()
                if MD5.get(modname) != md5sum(data):
                    skip = False
            if skip:
                continue
        importer(f"{NAME}.{modname}", f"{NAME}")
        MODS.append(modname)


importdir(DIR)


def __dir__():
    return MODS
