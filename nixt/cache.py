# This file is placed in the Public Domain.
# pylint: disable=C,W0105


"cache"


class Cache:

    objs = {}

    @staticmethod
    def add(path, obj):
        Cache.objs[path] = obj

    @staticmethod
    def get(path):
        return Cache.objs.get(path)

    @staticmethod
    def typed(matcher):
        for key in Cache.objs:
            if matcher not in key:
                continue
            yield Cache.objs.get(key)


"interface"


def __dir__():
    return (
        'Cache',
    )
