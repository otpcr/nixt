# This file is placed in the Public Domain.
# pylint: disable=C


"cache"


import _thread


cachelock = _thread.allocate_lock()


class Cache:

    objs = {}

    @staticmethod
    def add(path, obj):
        with cachelock:
            Cache.objs[path] = obj

    @staticmethod
    def get(path):
        with cachelock:
            return Cache.objs.get(path)

    @staticmethod
    def typed(matcher):
        with cachelock:
            for key in Cache.objs:
                if matcher not in key:
                    continue
                yield Cache.objs.get(key)
