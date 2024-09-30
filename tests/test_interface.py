# This file is placed in the Public Domain.
# pylint: disable=R,W0401,W0614,W0622
# ruff: noqa: F403,F405


"interface"


import logging
import sys
import unittest


import nixt


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
    'command',
    'method',
    'object',
    'persist',
    'runtime'
]


METHODS = [
    '__class__',
    '__contains__',
    '__delattr__',
    '__delitem__',
    '__dict__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__getitem__',
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
    '__setitem__',
    '__sizeof__',
    '__str__',
    '__subclasshook__',
    '__weakref__'
]


DIFF = [
    "__dict__",
    "__module__",
    "__slots__",
]


class TestInterface(unittest.TestCase):

    "TestInterface"

    def test_package(self):
        "test methods interface."
        okd = True
        for meth in PACKAGE:
            func1 = getattr(nixt, meth, None)
            if not func1:
                print(f"missing {meth}")
                okd = False
                break
        self.assertTrue(okd)


    def test_objects(self):
        "test methods interface."
        okd = True
        obj = Object()
        for meth in dir(obj):
            if meth not in METHODS:
                print(f"missing method {meth}")
                okd = False
        self.assertTrue(okd)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("SomeTest.testSomething").setLevel(logging.DEBUG)
    unittest.main()
