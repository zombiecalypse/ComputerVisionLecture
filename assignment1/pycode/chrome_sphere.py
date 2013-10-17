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
    xm = np.array(np.argmax(mask, axis=0).nonzero()).flatten()
    ym = np.array(np.argmax(mask, axis=1).nonzero()).flatten()
    # Horrible abuse of functions or pure genius - you decide.
    diam = np.mean([xm.shape[0], ym.shape[0]])
    cy = ym.mean()
    cx = xm.mean()
    return (np.array([cy, cx]), diam/2)

def locate_reflection(img):
    """Takes a masked img and returns the location position of the reflection."""
    arr = np.unravel_index(np.argmax(img), img.shape)
    return np.array(arr)

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

    d = (p-c)/R
    log.debug("Dir: %s", d)
    r = l.norm(d)
    theta = acos(r)
    log.debug(u"r:   %s", r)
    log.debug(u"θ:   %s", theta)

    n = np.hstack([d, [-sin(theta)]])
    return n

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        log.setLevel(logging.DEBUG)
    logging.basicConfig()
    mask = imread('../Images/chrome/chrome.mask.png', True)
    c, R = locate_ball(mask)
    for i in [22,23,24]: #range(12):
        name = '../Images/chrome/chrome.%i.png' % i
        log.info(name)
        img = imread(name, True)
        r = fit(img * mask, c, R)
        log.info("fit: %s", r)
