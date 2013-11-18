import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import pylab
from matplotlib.patches import CirclePolygon
from matplotlib.lines import Line2D
import scipy.linalg as l

import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import fun
fun.log.level = logging.INFO
from random import random

def cmap_as_list(cmap,n=20):
    if type(cmap) == str:
        cmap = pylab.get_cmap(cmap)
    p = np.linspace(0, 1, n)
    cols = cmap(p)
    return cols

class StereoVision(object):
    def __init__(self, l, r):
        self.imgl = mpimg.imread(l)
        self.imgr = mpimg.imread(r)
        self.fig = plt.figure()
        self.pointl = list(fun.P1)
        self.pointr = list(fun.P2)
        self.calculateF()
        #self.pointl = []
        #self.pointr= []
        self.F = None
        self.cmap = sorted(cmap_as_list('hsv'), key=lambda x:random())

    def plot_point(self, x, y, r):
        log.debug('x=%f, y=%f %s'%(x,y, r))

        circ = CirclePolygon((x,y), 5,
                             alpha=0.75)
        if r == 'r':
            col = self.cmap[len(self.pointr)%20]
            circ.set_color(col)
            self.ax1.add_patch(circ)
            self.pointr.append((x, y))
        else:
            col = self.cmap[len(self.pointl)%20]
            circ.set_color(col)
            self.ax2.add_patch(circ)
            self.pointl.append((x, y))
        if isinstance(self.F, np.ndarray):
            self.draw_line(x, y, r, col)
        self.fig.canvas.draw()

    def draw_line(self, x, y, r, col):
        assert isinstance(self.F, np.ndarray)
        # calculate second point p2 on epipolar line
        # p F x = 0
        p = np.array([x, y, 1])
        n = np.dot(self.F, p)
        log.info('n: %s', n)
        p1 = (-n[2]-self.imgl.shape[0])/n[1]
        p2 = (-n[2])/n[1]
        log.info('p1: %s p2: %s', p1, p2)
        # define a line in other image
        self.ax1.plot(p1/(p1+p2), (p2-p1)/(p1+p2))
        self.ax1.axis('image')

    def onclick(self, event):
        r = self.resolve(event.inaxes)
        try:
            self.plot_point(event.xdata, event.ydata, r)

            if len(self.pointr) > 7 and len(self.pointl) > 7 and self.F is None:
                self.calculateF()
        except Exception as e:
            log.error(e)

    def calculateF(self):
        self.F = 'calculate'
        log.info("Calculate F now...")
        minlen = min(len(self.pointl), len(self.pointr))
        self.F = fun.get_F(tuple(self.pointl[:minlen]), tuple(self.pointr[:minlen]))
        log.info("done...")
        log.info("F: %s", self.F)

    def resolve(self, ax):
        return "l" if ax == self.ax2 else "r"

    def plot(self):
        self.ax1 = self.fig.add_subplot(1, 2, 0)
        plt.imshow(self.imgl, cmap='gray')

        self.ax2 = self.fig.add_subplot(1, 2, 1)
        plt.imshow(self.imgr, cmap='gray')

        self.ax1.figure.canvas.mpl_connect('button_press_event', self.onclick)

        plt.show()

if __name__ == '__main__':
    import sys
    v = StereoVision(sys.argv[1], sys.argv[2])
    v.plot()
