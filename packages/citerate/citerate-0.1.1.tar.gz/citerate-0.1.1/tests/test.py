import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest

from citerate import citerator

DATA = [
    [10, 11, 12, 13, 14],
    [25, 2,  3,  4,  15],
    [24, 9,  1,  5,  16],
    [23, 8,  7,  6,  17],
    [22, 21, 20, 19, 18],
]

class CT(unittest.TestCase):
    def test_citerate(self, ):
        desired = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
        for i, value in enumerate(citerator(DATA, x=2, y=2)):
            assert value == desired[i]

    def test_citerate_layered(self, ):
        desired = [ [1],
                    [2, 3, 4, 5, 6, 7, 8, 9],
                    [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]]

        for i, layer in enumerate(citerator(DATA, x=2, y=2, layer=True)):
            assert layer == desired[i]

if __name__ == "__main__":
    unittest.main()

