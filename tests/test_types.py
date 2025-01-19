# This file is placed in the Public Domain.


"types"


import unittest


from nixt.objects import Object, dumps, loads


class ABC(Object):

    """ ABC """

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class BCD:

    """ BCD """

    def __init__(self):
        self.abc     = ABC()
        self.abc.bcd = ABC()
        self.abc.bcd.bla = ""

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class TestTypes(unittest.TestCase):

    """ TestTypes """

    def test_dumpload(self):
        """ dumps/loads test. """
        abc = True
        res = loads(dumps(abc))
        self.assertEqual(res, True)

    def test_string(self):
        """ string test. """
        abc = "yo!"
        res = loads(dumps(abc))
        self.assertEqual(res, "yo!")

    def test_integer(self):
        """ integer test. """
        abc = 1
        res = loads(dumps(abc))
        self.assertEqual(res, 1)

    def test_dict(self):
        """ dict test. """
        abc = {"a": "b"}
        res = loads(dumps(abc))
        self.assertEqual(res.a, "b")

    def test_boolean(self):
        """ boolean test. """
        abc = False
        res = loads(dumps(abc))
        self.assertEqual(res, False)

    def test_compsite(self):
        """ composite test. """
        bcd = BCD()
        bcd.abc.bcd.bla = 10
        res = loads(dumps(bcd))
        self.assertEqual(res.abc.bcd.bla, 10)
