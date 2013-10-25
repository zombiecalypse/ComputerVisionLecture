import unittest
from nose_parameterized import parameterized
from scipy.misc import imread
import chrome_sphere
import numpy as np

class ChromeTest(unittest.TestCase):
    def setUp(self):
        self.mask = imread('../Images/chrome/chrome.mask.png', True)
        self.c, self.R = chrome_sphere.locate_ball(self.mask)
        
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

    @parameterized.expand(enumerate([
            (0.3441,  -0.4300,  -0.8347),
            (0.2130,  -0.1223,  -0.9694),
            (0.2708,  -0.2654,  -0.9253),
            (0.0563,  -0.2280,  -0.9720),
            (-0.2423,  -0.4071,  -0.8807),
            (-0.2731,  -0.3663,  -0.8895),
            ( 0.3198, -0.3610, -0.8760),
            (-0.0094, -0.3012, -0.9535),
            ( 0.2074, -0.3342, -0.9194),
            ( 0.0891, -0.3298, -0.9398),
            ( 0.1281, -0.0443, -0.9908),
            (-0.1406, -0.3590, -0.9227),
       ]))
    def test_elements(self, i, x):
        x = np.array(x)
        name = '../Images/chrome/chrome.%i.png' % i
        img = imread(name, True)
        r = chrome_sphere.fit(img * self.mask, self.c, self.R)
        np.testing.assert_array_almost_equal(
                x, r, 1)
