# This file is placed in the Public Domain.


"a clean namespace"


import json


class Object:

    "Object"

    def __str__(self):
        return str(self.__dict__)


def construct(obj, *args, **kwargs):
    "constructor."
    if args:
        val = args[0]
        if isinstance(val, zip):
            update(obj, dict(val))
        elif isinstance(val, dict):
            update(obj, val)
        elif isinstance(val, Object):
            update(obj, vars(val))
    if kwargs:
        update(obj, kwargs)


def items(obj):
    "items."
    if isinstance(obj,type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj):
    "keys."
    if isinstance(obj, type({})):
        return obj.keys()
    return list(obj.__dict__.keys())


def update(obj, data):
    "update."
    if not isinstance(data, type({})):
        obj.__dict__.update(vars(data))
    else:
        obj.__dict__.update(data)


def values(obj):
    "values."
    return obj.__dict__.values()


class ObjectDecoder(json.JSONDecoder):

    "ObjectDecoder"

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, s, _w=None):
        "return constructed value from string."
        val = json.JSONDecoder.decode(self, s)
        if isinstance(val, dict):
            return hook(val)
        return val

    def raw_decode(self, s, idx=0):
        "decode from index."
        return json.JSONDecoder.raw_decode(self, s, idx)


def hook(objdict):
    "construct object from dict"
    obj = Object()
    construct(obj, objdict)
    return obj


def loads(string, *args, **kw):
    "load object from string."
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.loads(string, *args, **kw)


class ObjectEncoder(json.JSONEncoder):

    "ObjectEncoder"

    def __init__(self, *args, **kwargs):
        json.JSONEncoder.__init__(self, *args, **kwargs)

    def default(self, o):
        "return stringable representation."
        if isinstance(o, dict):
            return o.items()
        if issubclass(type(o), Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return vars(o)

    def encode(self, o) -> str:
        "encode object to string."
        return json.JSONEncoder.encode(self, o)

    def iterencode(self, o, _one_shot=False):
        "encode by piece."
        return json.JSONEncoder.iterencode(self, o, _one_shot)


def dumps(*args, **kw):
    "return string representation."
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)
