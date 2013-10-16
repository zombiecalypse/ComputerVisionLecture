from scipy.misc import imread
import numpy as np

def locate_ball(mask):
    """Returns ((center_x, center_y), radius) of the sphere."""
    radiusy, cy = max((len([i for i in r if i.all()]), j) for j,r in enumerate(mask))
    radiusx, cx = max((len([i for i in r if i.all()]), j) for j,r in enumerate(
        np.transpose(mask, (1, 0))))
    radius = (radiusy+radiusx)/2
    return ((cx, cy), radius)

def locate_reflection(img):
    """Takes a masked img and returns the location (x,y) of the reflection."""
    return np.unravel_index(np.argmax(img), img.shape)

def fit(image, mask):
    """Gives the direction of the light relative to the cam."""
    # First we need to find the center and the extend of the ball in 
    # order to evaluate where the light comes from.
    
    ((cx, cy), r) = locate_ball(mask)
    x, y = locate_reflection(image * mask)
    
    print "CoS: %s" % ((cx,cy),)
    print "RoS: %s" % (r,)
    print "PoL: %s" % ((x,y),)


if __name__ == '__main__':
    print fit(imread('../Images/chrome/chrome.0.png', True), imread('../Images/chrome/chrome.mask.png', True))
