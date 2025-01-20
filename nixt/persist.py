# This file is placed in the Public Domain.


"persistence"


import datetime
import json
import os
import pathlib
import _thread


from .methods import fqn
from .objects import dumps, loads, update


lock = _thread.allocate_lock()
p    = os.path.join


class DecodeError(Exception):

    """ DecodeError """


class Workdir:

    """ Workdir """

    wdr  = ""

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


def cdir(pth):
    """ create directory. """
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)



def long(name):
    """ extrapolate single name to full qualified name. """
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def pidname(name):
    """ return pidfile path. """
    return p(Workdir.wdr, f"{name}.pid")


def skel():
    """ skel directories. """
    path = pathlib.Path(store())
    path.mkdir(parents=True, exist_ok=True)
    return path


def store(pth=""):
    """ return store path, """
    return p(Workdir.wdr, "store", pth)


def types():
    """ return types in store. """
    return os.listdir(store())



def ident(obj):
    """ create an id. """
    return p(fqn(obj),*str(datetime.datetime.now()).split())


def read(obj, pth):
    """ read object from path. """
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            try:
                obj2 = loads(ofile.read())
                update(obj, obj2)
            except json.decoder.JSONDecodeError as ex:
                raise DecodeError(pth) from ex
    return pth


def write(obj, pth):
    """ write object to path. """
    with lock:
        cdir(pth)
        txt = dumps(obj, indent=4)
        with open(pth, 'w', encoding='utf-8') as ofile:
            ofile.write(txt)
    return pth


def __dir__():
    return (
        'Workdir',
        'cdir',
        'ident',
        'read',
        'skel',
        'write'
    )
