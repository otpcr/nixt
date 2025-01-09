# This file is placed in the Public Domain.


"runtime"


import os


from .object import Default


class Config(Default):

    name = Default.__module__.split(".")[0]
    wdr  = ""

    def __init__(self):
        Default.__init__(self)
        self.name = Config.name
        self.wdr  = self.wdr or os.path.expanduser(f"~/.{Config.name}")
