# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0105,W0622,E0402


"functions with the object as the first argument."


from .objects import get, items, keys, set


"methods"


def edit(obj, setter, skip=False):
    for key, val in items(setter):
        if skip and val == "":
            continue
        try:
            set(obj, key, int(val))
            continue
        except ValueError:
            pass
        try:
            set(obj, key, float(val))
            continue
        except ValueError:
            pass
        if val in ["True", "true"]:
            set(obj, key, True)
        elif val in ["False", "false"]:
            set(obj, key, False)
        else:
            set(obj, key, val)


def format(obj, args=None, skip=None, plain=False):
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
        value = get(obj, key, None)
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
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def match(obj, txt):
    for key in keys(obj):
        if txt in key:
            yield key


def search(obj, selector, matching=None):
    res = False
    if not selector:
        return res
    for key, value in items(selector):
        val = get(obj, key, None)
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
        'edit',
        'format',
        'fqn',
        'match',
        'search'
    )
