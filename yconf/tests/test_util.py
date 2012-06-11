# Copyright (c) 2012, Christian Kampka
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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

    def test_items(self):

        nd = NestedDict(self.data)

        for k, v in nd.items():
            self.assertIn(k, self.data)
            self.assertEqual(self.data[k], v)

    def test_parent(self):

        nd = NestedDict(self.data)
        self.assertEqual(nd, nd.a.parent)
        self.assertIsNone(nd.parent)

        nd.update({"parent": "foo"})
        self.assertIsNone(nd.parent)
        self.assertEqual("foo", nd.get("parent"))


    def test_in(self):

        nd = NestedDict(self.data)
        self.assertIn("a", nd)
        self.assertNotIn("g", nd)

    def test_delete(self):

        nd = NestedDict(self.data)


        self.assertIn("b", nd["a"])
        delattr(nd["a"], "b")
        self.assertNotIn("b", nd["a"])

        self.assertIn("e", nd["a"])
        del nd["a"]["e"]
        self.assertNotIn("e", nd["a"])

        self.assertIn("a", nd)
        nd.delete("a")
        self.assertNotIn("a", nd)


def test_suite():
    from unittest import TestLoader
    return TestLoader().loadTestsFromName(__name__)
