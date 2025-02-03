# This file is placed in the Public Domain.


"encoder"


import json


from .objects import Object


class ObjectEncoder(json.JSONEncoder):

    def __init__(self, *args, **kwargs):
        json.JSONEncoder.__init__(self, *args, **kwargs)

    def default(self, o):
        if isinstance(o, dict):
            return o.items()
        if issubclass(type(o), Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            try:
                return vars(o)
            except TypeError:
                return repr(o)

    def encode(self, o) -> str:
        return json.JSONEncoder.encode(self, o)

    def iterencode(self, o, _one_shot=False):
        return json.JSONEncoder.iterencode(self, o, _one_shot)


def dumps(*args, **kw):
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)


def __dir__():
    return (
        'ObjectEncoder',
        'dumps'
    )
