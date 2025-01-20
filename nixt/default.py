# This file is placed in the Public Domain.


"default"


class Default:

    """ Default """

    default = ""

    def __contains__(self, key):
        return key in dir(self)

    def __getattr__(self, key):
        return self.__dict__.get(key, self.default)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    @staticmethod
    def getdefault():
        """ return default. """
        return Default.default

    @staticmethod
    def setdefault(default):
        """ set default. """
        Default.default = default


class Config(Default):

    """ Config """

    dis  = "upt"
    mods = ""
    name = Default.__module__.split(".", maxsplit=1)[0]


def __dir__():
    return (
        'Config',
        'Default'
    )
