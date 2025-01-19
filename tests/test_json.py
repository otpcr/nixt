# This file is placed in the Public Domain.


"json"


import unittest


from nixt.objects import Object, dumps, loads


VALIDJSON = "{'test': 'bla'}"
VALIDPYTHON = '{"test": "bla"}'


class TestDecoder(unittest.TestCase):

    """ TestDecoder """

    def test_loads(self):
        """ loads test. """
        obj = Object()
        obj.test = "bla"
        oobj = loads(dumps(obj))
        self.assertEqual(oobj.test, "bla")


class TestEncoder(unittest.TestCase):

    """ TestEncoder """

    def test_dumps(self):
        """ dumps test. """
        obj = Object()
        obj.test = "bla"
        self.assertEqual(dumps(obj), VALIDPYTHON)
