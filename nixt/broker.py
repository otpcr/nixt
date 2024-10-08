# This file is placed in the Public Domain.
# pylint: disable=W0105


"broker"


class Broker:

    "Broker"

    objs = {}

    @staticmethod
    def add(obj):
        "add object."
        Broker.objs[repr(obj)] = obj

    @staticmethod
    def announce(txt, kind=None):
        "announce text on brokered objects."
        for obj in Broker.all(kind):
            if "announce" in dir(obj):
                obj.announce(txt)

    @staticmethod
    def all(kind=None):
        "return all objects."
        result = []
        if kind is not None:
            for key in [x for x in Broker.objs if kind in x]:
                result.append(Broker.get(key))
        else:
            result.extend(list(Broker.objs.values()))
        return result

    @staticmethod
    def get(orig):
        "return object by matching repr."
        return Broker.objs.get(orig)


"interface"


def __dir__():
    return (
        'Broker',
    )
