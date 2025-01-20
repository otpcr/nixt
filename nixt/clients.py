# This file is placed in the Public Domain.
# pylint: disable=W0105


"clients"


from .caching import Fleet
from .command import command
from .runtime import Reactor


"client"


class Client(Reactor):

    """ Client """

    def __init__(self):
        Reactor.__init__(self)
        self.register("command", command)
        Fleet.add(self)

    def raw(self, txt):
        """ echo text. """
        raise NotImplementedError("raw")

    def say(self, _channel, txt):
        """ relay to raw. """
        self.raw(txt)


"interface"


def __dir__():
    return (
        'Client',
    )
