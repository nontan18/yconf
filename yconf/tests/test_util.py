
from testtools import TestCase
from testtools.matchers import IsInstance

from yconf.util import NestedDict


class ConfigEntryTest(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.data = self.data = {"a": {"b": {"c": "d"}, "e": "f"}}

    def test_dictAccess(self):

        nd = NestedDict(self.data)

        self.assertThat(nd["a"], IsInstance(NestedDict))
        self.assertEqual(nd["a"].data, self.data["a"])
        self.assertEqual(nd["a"]["e"], "f")
        self.assertEqual(nd["a"]["b"]["c"], "d")

    def test_attrAccess(self):
        nd = NestedDict(self.data)

        self.assertThat(nd.a, IsInstance(NestedDict))
        self.assertEqual(nd.a.data, self.data["a"])
        self.assertEqual(nd.a.e, nd["a"]["e"])
        self.assertEqual(nd.a.b.c, "d")

    def test_setattr(self):
        nd = NestedDict()
        setattr(nd, "a.b.c", "d")

        self.assertEqual("d", nd.data["a"]["b"]["c"])

    def test_get(self):

        nd = NestedDict(self.data)

        self.assertThat(nd.get("a"), IsInstance(NestedDict))
        self.assertEqual(nd.get("a").data, self.data["a"])
        self.assertEqual(nd.get("a").get("e"), nd["a"]["e"])
        self.assertEqual(nd.a.get("b").c, "d")

        self.assertIsNone(nd.get("x"), None)
        self.assertEqual(nd.get("x", "y"), "y")

    def test_has(self):

        nd = NestedDict(self.data)

        self.assertTrue(nd.has("a"))
        self.assertFalse(nd.has("b"))
        self.assertFalse(nd.has("parent"))

    def test_call(self):

        nd = NestedDict(self.data)

        self.assertEqual(self.data, nd())
        self.assertEqual(self.data["a"], nd.a())

    def test_update(self):

        nd = NestedDict({})
        nd.update(self.data)
        nd.update({"a": {"b": {"i": "j"}}})
        nd.update({"a": {"b": {"c": "x"}}})
        nd.update({"a": {"g": "h"}})

        self.assertTrue(nd.a.has("g"))
        self.assertTrue(nd.a.b.has("c"))
        self.assertEqual(nd.a.b.c, "x")
        self.assertTrue(nd.a.b.has("i"))
        self.assertEqual(nd.a.b.i, "j")
        self.assertEqual(nd.a.g, "h")
        self.assertEqual(nd.a.e, "f")

    def test_lookup(self):

        nd = NestedDict(self.data)

        self.assertEqual("d", nd.lookup(("a", "b", "c")))
        self.assertIsNone(None, nd.lookup(("a", "x", "y")))
        self.assertEqual(self.data["a"], nd.lookup(["a"]))

    def test_iteritems(self):

        nd = NestedDict(self.data)

        for k, v in nd.iteritems():
            self.assertIn(k, self.data)
            self.assertEqual(self.data[k], v)

    def test_parent(self):

        nd = NestedDict(self.data)
        self.assertEqual(nd, nd.a.parent)
        self.assertIsNone(nd.parent)

        nd.update({"parent": "foo"})
        self.assertIsNone(nd.parent)
        self.assertEqual("foo", nd.get("parent"))


def test_suite():
    from unittest import TestLoader
    return TestLoader().loadTestsFromName(__name__)
