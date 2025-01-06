# This file is placed in the Public Domain.


"client"


from .command import command
from .reactor import Reactor


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        self.register("command", command)

    def raw(self, txt):
        raise NotImplementedError("raw")

