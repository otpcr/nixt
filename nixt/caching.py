# This file is placed in the Public Domain.


""" caching

Contains the Cache class that has class level objects in it's cache.
Index into the cache is a file path so it can be mapped to disk.

Operatings are done on the Cache class it self:

add an object:

    >>> from nixt.objects import Object
    >>> from nixt.caching import Cache
    >>> o = Object()
    >>> Cache.add("filename", o)
    >>> 

retrieving goes with get:

    >>> Cache.get("filename")
    <nixt.objects.Object object at 0x7feefa981e90>

matching by key goes with the typed method:

    >>> Cache.typed("filename")
    <generator object Cache.typed at 0x7feefa73be60>

this cache is mostely used to have object couple to a file with a
pathname on the disk.

"""


import typing


class Cache:

    """ Cache """

    objs = {}

    @staticmethod
    def add(path, obj) -> None:
        "add object with path."
        Cache.objs[path] = obj

    @staticmethod
    def get(path) -> typing.Any:
        "get object by path."
        return Cache.objs.get(path, None)

    @staticmethod
    def typed(matcher) -> [typing.Any]:
        "get objects by type."
        for key in Cache.objs:
            if matcher not in key:
                continue
            yield Cache.objs.get(key)


def __dir__():
    return (
        'Cache',
    )
