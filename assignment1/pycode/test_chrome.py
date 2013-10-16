import unittest
import chrome_sphere
import numpy as np

class ChromeTest(unittest.TestCase):
    def test_location_simple(self):
        np.testing.assert_array_equal(
                np.array([1,0]),
                chrome_sphere.locate_reflection(np.array([
                    [0,0,0,0],
                    [1,0,0,0],
                    [0,0,0,0],
                ])))
    def test_location_noisy(self):
        np.testing.assert_array_equal(
                np.array([1,0]),
                chrome_sphere.locate_reflection(np.array([
                    [0,.8,0,0],
                    [1,0,.9,0],
                    [0,0,0,0],
                ])))
