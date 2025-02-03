# This file is placed in the Public Domain.


"decoding"


import json


from .objects import Object, construct


class ObjectDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, s, _w=None):
        val = json.JSONDecoder.decode(self, s)
        if isinstance(val, dict):
            return hook(val)
        return val

    def raw_decode(self, s, idx=0):
        return json.JSONDecoder.raw_decode(self, s, idx)


def hook(objdict):
    obj = Object()
    construct(obj, objdict)
    return obj


def loads(string, *args, **kw):
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.loads(string, *args, **kw)



def __dir__():
    return (
        'ObjectDecoder',
        'hook',
        'loads'
    )
