# This file is placed in the Public Domain.
# pylint: disable=R,W0105


"default values"


from . import Object


class Default(Object):

    "Default"

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


class Config(Default):

    "Config"


"interface"


def __dir__():
    return (
        'Config',
        'Default'
    )
