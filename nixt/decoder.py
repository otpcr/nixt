# This file is placed in the Public Domain.


"object decoding"

import json


from typing import Any


from .objects import Object, construct


class ObjectDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, s, _w=None) -> Any:
        val = json.JSONDecoder.decode(self, s)
        if isinstance(val, dict):
            return hook(val)
        return val


def hook(objdict) -> Object:
    obj = Object()
    construct(obj, objdict)
    return obj


def loads(string, *args, **kw) -> Object:
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.loads(string, *args, **kw)


def __dir__():
    return (
        'ObjectDecoder',
        'hook',
        'loads'
    )
