# This file is placed in the Public Domain.


"composite"


import unittest


from nixt.objects import Object


class TestComposite(unittest.TestCase):

    """ TestComposite """

    def testcomposite(self):
        """ composite test. """
        obj = Object()
        obj.obj = Object()
        obj.obj.abc = "test"
        self.assertEqual(obj.obj.abc, "test")
