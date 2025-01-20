# This file is placed in the Public Domain.
# pylint: disable=W0105


"a clean namespace"


import json


"object"


class Object:

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


"decoder"


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


"encoder"


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


"methods"


def edit(obj, setter, skip=False):
    """ edit by setter dict."""
    for key, val in items(setter):
        if skip and val == "":
            continue
        try:
            setattr(obj, key, int(val))
            continue
        except ValueError:
            pass
        try:
            setattr(obj, key, float(val))
            continue
        except ValueError:
            pass
        if val in ["True", "true"]:
            setattr(obj, key, True)
        elif val in ["False", "false"]:
            setattr(obj, key, False)
        else:
            setattr(obj, key, val)


def fmt(obj, args=None, skip=None, plain=False):
    """ format for output. """
    if args is None:
        args = keys(obj)
    if skip is None:
        skip = []
    txt = ""
    for key in args:
        if key.startswith("__"):
            continue
        if key in skip:
            continue
        value = getattr(obj, key, None)
        if value is None:
            continue
        if plain:
            txt += f"{value} "
        elif isinstance(value, str) and len(value.split()) >= 2:
            txt += f'{key}="{value}" '
        else:
            txt += f'{key}={value} '
    return txt.strip()


def fqn(obj):
    """ full qualified name. """
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def match(obj, txt):
    """ match by key. """
    for key in keys(obj):
        if txt in key:
            yield key


def search(obj, selector, matching=None):
    """ match by selector dict. """
    res = False
    if not selector:
        return res
    for key, value in items(selector):
        val = getattr(obj, key, None)
        if not val:
            continue
        if matching and value == val:
            res = True
        elif str(value).lower() in str(val).lower() or value == "match":
            res = True
        else:
            res = False
            break
    return res


"interface"


def __dir__():
    return (
         'Object',
         'construct',
         'dumps',
         'edit',
         'fmt',
         'fqn',
         'items',
         'keys',
         'loads',
         'match',
         'search'
         'update',
         'values'
    )
