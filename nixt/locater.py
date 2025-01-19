# This file is placed in the Public Domain.
# pylint: disable=W0105,E0402


"locator"


import datetime
import os
import threading
import time


from .object  import Object, fqn, search, update
from .persist import long, skel, read, store


"defines"


lock = threading.RLock()
p    = os.path.join


"cache"


class Cache:

    """ Cache """

    objs = {}

    @staticmethod
    def add(path, obj):
        """ add object to cache. """
        Cache.objs[path] = obj

    @staticmethod
    def get(path):
        """ get object from cache. """
        return Cache.objs.get(path, None)

    @staticmethod
    def typed(matcher):
        """ match typed objects. """
        for key in Cache.objs:
            if matcher not in key:
                continue
            yield Cache.objs.get(key)


"find"


def fns(clz):
    """ return filenames by class. """
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
    """ find objects by class and selector dict. """
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


"utilities"


def elapsed(seconds, short=True):
    """ return elapsed string from seconds. """
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
    """ derive time from filename. """
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
    """ strip from end of path. """
    return os.sep.join(pth.split(os.sep)[-nmr:])


"methods"


def ident(obj):
    """ create an id. """
    return p(fqn(obj),*str(datetime.datetime.now()).split())


def last(obj, selector=None):
    """ return last object of a type. """
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


"interface"


def __dir__():
    return (
        'Cache',
        'elapsed',
        'find',
        'last'
    )
