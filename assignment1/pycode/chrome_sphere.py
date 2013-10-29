# -*- coding: utf8 -*-
from math import *
from scipy.misc import imread
from scipy import linalg as l
from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
import logging
log = logging.getLogger(__name__)

def locate_ball(mask):
    """Returns (center, radius) of the sphere."""
    xm = np.array(np.argmax(mask, axis=1).nonzero()).flatten()
    ym = np.array(np.argmax(mask, axis=0).nonzero()).flatten()
    # Horrible abuse of functions or pure genius - you decide.
    diam = np.mean([xm.shape[0], ym.shape[0]])
    cy = ym.mean()
    cx = xm.mean()
    return (np.array([cx, cy, 0]), diam/2)

def locate_reflection(img):
    """Takes a masked img and returns the location position of the reflection."""
    arr = np.unravel_index(np.argmax(img), img.shape)
    return np.array(arr+(0, ))

def fit(image, c, R):
    """Gives the direction of the light relative to the scene."""
    # Since we're using the brightest pixel, we want to ensure that the
    # neighbourhood is bright as well.
    image = ndimage.gaussian_filter(image, sigma=2)

    # First we need to find the center and the extend of the ball in 
    # order to evaluate where the light comes from.
    #

    p = locate_reflection(image)

    log.debug("CoS: %s", c)
    log.debug("RoS: %s", R)
    log.debug("PoL: %s", p)

    # The d coordinate system is relative to the center of the sphere.

    d = (p-c)
    d_normalized = d/R
    log.debug("Dir: %s (|.| = %.3f", d, l.norm(d))

    d_normalized[2] = -sqrt(1**2-l.norm(d_normalized)**2)

    log.debug("|d_n| = %.3f", l.norm(d_normalized))

    n= d_normalized

    ret = 2*np.dot(n,d_normalized)*n - d_normalized
    log.debug("ret = %s", ret)
    return ret

example = np.array([
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
            ])

def run():
    mask = imread('../Images/chrome/chrome.mask.png', True)
    c, R = locate_ball(mask)
    l = np.zeros([12, 3])
    for i in range(12):
        name = '../Images/chrome/chrome.%i.png' % i
        log.info(name)
        img = imread(name, True)
        l[i] = fit(img * mask, c, R)

    return l

if __name__ == '__main__':
    l = run()
    print "\\\\\n".join("&".join("%.3f" % x for x in t) for t in l)

