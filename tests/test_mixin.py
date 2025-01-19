# This file is placed in the Public Domain.


"mixin"


import unittest


from nixt.objects import Object


class Mix:

    """ Mix """

    a = "b"

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class Mixin(Mix, Object):

    """ Mixin """

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class TestMixin(unittest.TestCase):

    """ TestMixin """

    def test_mixin(self):
        """ mixin test. """
        mix = Mixin()
        self.assertTrue(isinstance(mix, Mixin))
