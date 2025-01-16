# This file is placed in the Public Domain.


"persistence"


import json
import os
import pathlib
import time
import _thread


from .methods import fqn, search
from .objects import Object, dumps, loads, update


lock   = _thread.allocate_lock()
p      = os.path.join
rwlock = _thread.allocate_lock()


class DecodeError(Exception):

    "DecodeError"


class EncodeError(Exception):

    "EncodeError"


class Workdir:

    "Workdir"

    wdr  = ""


class Cache:

    "Cache"

    objs = {}

    @staticmethod
    def add(path, obj):
        "add object with its path."
        Cache.objs[path] = obj

    @staticmethod
    def get(path):
        "return object by path."
        return Cache.objs.get(path, None)

    @staticmethod
    def typed(matcher):
        "return cached object by type."
        for key in Cache.objs:
            if matcher not in key:
                continue
            yield Cache.objs.get(key)


def long(name):
    "return fqn name from store."
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def pidname(name):
    "return pidfile in workdir."
    return p(Workdir.wdr, f"{name}.pid")


def skel():
    "create necessary files."
    path = pathlib.Path(store())
    path.mkdir(parents=True, exist_ok=True)
    return path


def store(pth=""):
    "return path to store."
    return p(Workdir.wdr, "store", pth)


def types():
    "return all types in store."
    return os.listdir(store())


def fns(clz):
    "find all matching paths."
    dname = ''
    pth = store(clz)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        if dirs:
            for dname in sorted(dirs):
                if dname.count('-') == 2:
                    ddd = p(rootdir, dname)
                    for fll in os.listdir(ddd):
                        yield p(ddd, fll)


def find(clz, selector=None, deleted=False, matching=False):
    "find matching objects."
    skel()
    with lock:
        pth = long(clz)
        res = []
        for fnm in fns(pth):
            obj = Cache.get(fnm)
            if not obj:
                obj = Object()
                read(obj, fnm)
                Cache.add(fnm, obj)
            if not deleted and '__deleted__' in dir(obj) and obj.__deleted__:
                continue
            if selector and not search(obj, selector, matching):
                continue
            res.append((fnm, obj))
        return res


def last(obj, selector=None):
    "return last object."
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    res = None
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        res = inp[0]
    return res


def read(obj, pth):
    "read object from path."
    with rwlock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            try:
                obj2 = loads(ofile.read())
                update(obj, obj2)
            except json.decoder.JSONDecodeError as ex:
                raise DecodeError(pth) from ex
    return pth


def write(obj, pth):
    "Write to path/"
    with rwlock:
        cdir(pth)
        txt = dumps(obj, indent=4)
        with open(pth, 'w', encoding='utf-8') as ofile:
            ofile.write(txt)
    return pth


def cdir(pth):
    "create directory."
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


def elapsed(seconds, short=True):
    "show string representing elapsed time (seconds)."
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    yea = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    yeas = int(nsec/yea)
    nsec -= yeas*yea
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    nsec -= int(minute*minutes)
    sec = int(nsec)
    if yeas:
        txt += f"{yeas}y"
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += f"{nrdays}d"
    if short and txt:
        return txt.strip()
    if hours:
        txt += f"{hours}h"
    if minutes:
        txt += f"{minutes}m"
    if sec:
        txt += f"{sec}s"
    txt = txt.strip()
    return txt


def fntime(daystr):
    "extract time from filename."
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    return timed


def strip(pth, nmr=3):
    "right strip path."
    return os.sep.join(pth.split(os.sep)[-nmr:])


def __dir__():
    return (
        'Cache',
        'Workdir',
        'cdir',
        'elapsed',
        'find',
        'last',
        'read',
        'skel',
        'write'
    )
