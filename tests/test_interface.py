# This file is placed in the Public Domain.
# pylint: disable=C,R,W0401,W0614,W0622
# ruff: noqa: F403,F405


"interface"


import logging
import sys
import unittest


import nixt
import nixt.object
import nixt.persist
import nixt.runtime


from nixt.object import *


PACKAGE = [
    '__builtins__',
    '__cached__',
    '__doc__',
    '__file__',
    '__loader__',
    '__name__',
    '__package__',
    '__path__',
    '__spec__',
    'object',
    'persist',
    'runtime'
]


METHODS = [
    '__class__',
    '__contains__',
    '__delattr__',
    '__dict__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__getstate__',
    '__gt__',
    '__hash__',
    '__init__',
    '__init_subclass__',
    '__iter__',
    '__le__',
    '__len__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__setattr__',
    '__sizeof__',
    '__str__',
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
                break
        self.assertTrue(okd)

    def test_objects(self):
        okd = True
        obj = Object()
        dirr = dir(obj)
        for meth in METHODS:
            if meth not in dirr:
                okd = False
        self.assertTrue(okd)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("SomeTest.testSomething").setLevel(logging.DEBUG)
    unittest.main()
