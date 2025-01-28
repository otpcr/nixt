# This file is placed in the Public Domain.
# pylint: disable=W0611
# ruff: noqa: F401


"interface"


import os


SKIP = ["wsd.py",]
MODS = sorted([
               x[:-3] for x in os.listdir(os.path.dirname(__file__))
               if x.endswith(".py") and not x.startswith("__")
               and x not in SKIP
              ])


def __dir__():
    return MODS
