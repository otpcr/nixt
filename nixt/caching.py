# This file is placed in the Public Domain.


"caching"


class Cache:

    objs = {}

    @staticmethod
    def add(path, obj):
        Cache.objs[path] = obj

    @staticmethod
    def get(path):
        return Cache.objs.get(path, None)

    @staticmethod
    def typed(matcher):
        for key in Cache.objs:
            if matcher not in key:
                continue
            yield Cache.objs.get(key)


def __dir__():
    return (
        'Cache',
    )
