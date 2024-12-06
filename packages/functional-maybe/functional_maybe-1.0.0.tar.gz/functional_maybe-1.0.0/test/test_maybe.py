import unittest
from src.functional_maybe import FunctionalMaybe as Maybe

from typing import NamedTuple


PRINT = False


class Tst(NamedTuple):
    x: int
    y: str


def logger(val):
    # Just to console
    return print(val) if PRINT else None


TEST_PARAMS = (1, "one")


def constructTestMaybe():
    return Maybe().construct(type_=Tst, params=TEST_PARAMS)


class TestMaybe(unittest.TestCase):
    def testConstructor(self):
        self.assertEqual(str(constructTestMaybe().get()), str(Tst(*TEST_PARAMS)))

    def testTransform(self):
        self.assertEqual(constructTestMaybe().transform(lambda i, s: str(i) + " " + s, True).get(),
                         (lambda i, s: str(i) + " " + s)(*TEST_PARAMS))

    def testRun(self):
        self.assertEqual(constructTestMaybe().run(lambda _: 1).get(), constructTestMaybe().get())
