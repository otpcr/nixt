# This file is placed in the Public Domain.


"a clean namespace"


import json


"object"


class Object: # pylint: disable=R0902


    """ Object """


    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


def construct(obj, *args, **kwargs):
    """ construct object from arguments. """
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
    """ return items. """
    if isinstance(obj,type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj):
    """ return keys. """
    if isinstance(obj, type({})):
        return obj.keys()
    return list(obj.__dict__.keys())


def update(obj, data):
    """ update object. """
    if not isinstance(data, type({})):
        obj.__dict__.update(vars(data))
    else:
        obj.__dict__.update(data)


def values(obj):
    """ return values, """
    return obj.__dict__.values()



class ObjectDecoder(json.JSONDecoder):

    """ ObjectDecoder """

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, s, _w=None):
        """ create from string. """
        val = json.JSONDecoder.decode(self, s)
        if isinstance(val, dict):
            return hook(val)
        return val

    def raw_decode(self, s, idx=0):
        """ create piecemale. """
        return json.JSONDecoder.raw_decode(self, s, idx)


def dumps(*args, **kw):
    """ dump object to string. """
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)


def hook(objdict):
    """ construct object from dict. """
    obj = Object()
    construct(obj, objdict)
    return obj


class ObjectEncoder(json.JSONEncoder):

    """ ObjectEncoder """

    def __init__(self, *args, **kwargs):
        json.JSONEncoder.__init__(self, *args, **kwargs)

    def default(self, o):
        """ return stringable value. """
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


def loads(string, *args, **kw):
    """ load object from string. """
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.loads(string, *args, **kw)


def __dir__():
    return (
         'Object',
         'construct',
         'dumps',
         'items',
         'keys',
         'loads',
         'update',
         'values'
    )
