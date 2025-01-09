# This file is placed in the Public Domain.
# pylint: disable=C,R,W0401,W0614,W0622
# ruff: noqa: F403,F405


"interface"


import logging
import sys
import unittest


import nixt


from nixt.object import *


import nixt.cache
import nixt.client
import nixt.command
import nixt.default
import nixt.error
import nixt.event
import nixt.find
import nixt.modules
import nixt.object
import nixt.output
import nixt.reactor
import nixt.thread


PACKAGE = [
    'cache',
    'client',
    'command',
    'default',
    'error',
    'event',
    'find',
    'modules',
    'object',
    'output',
    'reactor',
    'thread'
]


METHODS = [
    '__class__',
    '__delattr__',
    '__dict__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__gt__',
    '__hash__',
    '__init__',
    '__init_subclass__',
    '__le__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__setattr__',
    '__sizeof__',
    '__subclasshook__',
    '__weakref__'
]


class TestInterface(unittest.TestCase):

    def test_package(self):
        okd = True
        for mod in PACKAGE:
            mod1 = getattr(nixt, mod, None)
            if not mod1:
                okd = False
                print(mod)
                break
        self.assertTrue(okd)

    def test_objects(self):
        okd = True
        obj = Object()
        dirr = dir(obj)
        print(dirr)
        for meth in METHODS:
            if meth not in dirr:
                okd = False
                print(f"{meth} not found")
        self.assertTrue(okd)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("SomeTest.testSomething").setLevel(logging.DEBUG)
    unittest.main()
