# This file is placed in the Public Domain.


"methods"


from .objects import items, keys


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


def __dir__():
    return (
         'edit',
         'fmt',
         'fqn',
         'match',
         'search'
    )
