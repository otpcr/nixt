# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0622


"objects"


import unittest


from nixt.object import Object, items, keys, update, values


import nixt.object


VALIDJSON = '{"test": "bla"}'


attrs1 = (
    'Object',
    'Obj',
    'construct',
    'dumps',
    'edit',
    'format',
    'fqn',
    'items',
    'keys',
    'loads',
    'match',
    'search',
    'update',
    'values'
)


attrs2 = (
    '__doc__',
    '__lt__',
    '__init__',
    '__setattr__',
    '__ne__',
    '__delattr__',
    '__eq__',
    '__dir__',
    '__new__',
    '__iter__',
    '__reduce__',
    '__class__',
    '__module__',
    '__gt__',
    '__str__',
    '__init_subclass__',
    '__reduce_ex__',
    '__dict__',
    '__subclasshook__',
    '__le__',
    '__contains__',
    '__weakref__',
    '__ge__',
    '__sizeof__',
    '__getattribute__',
    '__format__',
    '__len__',
    '__getstate__',
    '__repr__',
    '__hash__'
)


OBJECT  = Object()
PACKAGE = nixt.object


class TestObject(unittest.TestCase):


    "Object related tests."


    def test_attributes(self):
        okd = True
        for meth in attrs2:
            print(meth)
            mth = getattr(OBJECT, meth, None)
            if mth is None:
                okd = meth
        self.assertTrue(okd)

    def test_constructor(self):
        "constructor test."
        obj = Object()
        self.assertTrue(type(obj), Object)

    def test_class(self):
        "test proper class."
        obj = Object()
        clz = obj.__class__()
        self.assertTrue("Object" in str(type(clz)))

    def test_contains(self):
        "test containment."
        obj = Object()
        obj.key = "value"
        self.assertTrue("key" in obj)

    def test_delattr(self):
        "test deleting of attribute."
        obj = Object()
        obj.key = "value"
        del obj.key
        self.assertTrue("key" not in obj)

    def test_dict(self):
        "test __dict__"
        obj = Object()
        self.assertEqual(obj.__dict__, {})

    def test_fmt(self):
        "test __format__"
        obj = Object()
        self.assertEqual(format(obj), '{}')

    def test_format(self):
        "test object format."
        obj = Object()
        self.assertEqual(format(obj), '{}')

    def test_getattribute(self):
        "test attributing."
        obj = Object()
        obj.key = "value"
        self.assertEqual(obj.__getattribute__("key"), "value")

    def test_getattr(self):
        "test retrieving of attributes."
        obj = Object()
        obj.key = "value"
        self.assertEqual(getattr(obj, "key"), "value")

    def test_hash(self):
        "test for hash being an integer."
        obj = Object()
        hsj = hash(obj)
        self.assertTrue(isinstance(hsj, int))

    def test_init(self):
        "test constructor."
        obj = Object()
        self.assertTrue(type(Object.__init__(obj)), Object)

    def test_items(self):
        "test items of object."
        obj = Object()
        obj.key = "value"
        self.assertEqual(
            list(items(obj)),
            [
                ("key", "value"),
            ],
        )

    def test_iter(self):
        "test iteration."
        obj = Object()
        obj.key = "value"
        self.assertTrue(
            list(obj.__iter__()),
            [
                "key",
            ],
        )

    def test_keys(self):
        "test returning of keys."
        obj = Object()
        obj.key = "value"
        self.assertEqual(
            list(keys(obj)),
            [
                "key",
            ],
        )

    def test_len(self):
        "test length calcualtion."
        obj = Object()
        self.assertEqual(len(obj), 0)

    def test_methods(self):
        okd = True
        for attr in attrs1:
            att = getattr(PACKAGE, attr, None)
            if not att:
                okd = attr
                break
        self.assertTrue(okd)

    def test_module(self):
        "test module name."
        self.assertEqual(Object().__module__, "nixt.object")

    def test_register(self):
        "test setting attribute."        
        obj = Object()
        setattr(obj, "key", "value")
        self.assertEqual(obj.key, "value")

    def test_repr(self):
        "test representation."
        self.assertTrue(update(Object(), {"key": "value"}).__repr__(), {"key": "value"})

    def test_setattr(self):
        "test setting of attribute."
        obj = Object()
        obj.__setattr__("key", "value")
        self.assertTrue(obj.key, "value")

    def test_str(self):
        "test stringify."
        obj = Object()
        self.assertEqual(str(obj), "{}")

    def test_update(self):
        "test updating of object."
        obj = Object()
        obj.key = "value"
        oobj = Object()
        update(oobj, obj)
        self.assertTrue(oobj.key, "value")

    def test_values(self):
        "test values of an object."
        obj = Object()
        obj.key = "value"
        self.assertEqual(
            list(values(obj)),
            [
                "value",
            ],
        )
