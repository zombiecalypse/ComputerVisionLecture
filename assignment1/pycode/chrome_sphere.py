# -*- coding: utf8 -*-
from math import *
from scipy.misc import imread
from scipy import linalg as l
import numpy as np
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def locate_ball(mask):
    """Returns ((center_x, center_y), radius) of the sphere."""
    radiusy, cy = max((len([i for i in r if i.all()]), j) for j,r in enumerate(mask))
    radiusx, cx = max((len([i for i in r if i.all()]), j) for j,r in enumerate(
        np.transpose(mask, (1, 0))))
    radius = (radiusy+radiusx)/2
    return (np.array([cx, cy]), float(radius))

def locate_reflection(img):
    """Takes a masked img and returns the location (x,y) of the reflection."""
    arr = np.unravel_index(np.argmax(img), img.shape)
    return np.array([arr[1],arr[0]])

def fit(image, mask):
    """Gives the direction of the light relative to the scene."""
    # First we need to find the center and the extend of the ball in 
    # order to evaluate where the light comes from.

    c, R = locate_ball(mask)
    p = locate_reflection(image * mask)

    log.debug("CoS: %s", c)
    log.debug("RoS: %s", R)
    log.debug("PoL: %s", p)

    # The d coordinate system is relative to the center of the sphere.

    d = (p-c)/R
    log.debug("Dir: %s", d)
    phi = atan2(d[1], d[0])
    r = l.norm(d)
    theta = acos(r)
    log.debug(u"r:   %s", r)
    log.debug(u"θ:   %s", theta)
    log.debug(u"φ:   %s", phi)

    return np.array([
            sin(theta)*cos(phi),
            -cos(theta),
            sin(theta)*sin(phi),
    ])

if __name__ == '__main__':
    logging.basicConfig()
    mask = imread('../Images/chrome/chrome.mask.png', True)
    for i in [3]:# range(12):
        print fit(imread('../Images/chrome/chrome.%i.png' % i, True), mask)
