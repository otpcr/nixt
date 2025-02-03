# This file is placed in the Public Domain.


"working directory"


import os
import pathlib


p = os.path.join


class Workdir:

    wdr  = ""


def long(name):
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def pidname(name):
    return p(Workdir.wdr, f"{name}.pid")


def skel():
    path = pathlib.Path(store())
    path.mkdir(parents=True, exist_ok=True)
    return path


def store(pth=""):
    return p(Workdir.wdr, "store", pth)


def strip(pth, nmr=3):
    return os.sep.join(pth.split(os.sep)[-nmr:])

def types():
    return os.listdir(store())


def __dir__():
    return (
        'Workdir',
        'long',
        'pidname',
        'skel',
        'store',
        'types'
    )
