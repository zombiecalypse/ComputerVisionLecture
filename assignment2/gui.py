import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import pylab
from matplotlib.patches import CirclePolygon

import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import fun
fun.log.level = logging.INFO
from random import shuffle

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
        self.pointl = []
        self.pointr = []
        self.F = None
        self.cmap = cmap_as_list('hsv')
        shuffle(self.cmap)

    def onclick(self, event):
        r = self.resolve(event.inaxes)
        try:
            log.debug('x=%f, y=%f %s'%(event.xdata, event.ydata, r))

            circ = CirclePolygon((event.xdata, event.ydata), 5,
                                 alpha=0.75)
            if r == 'r':
                col = self.cmap[len(self.pointr)]
                circ.set_color(col)
                self.ax1.add_patch(circ)
                self.pointr.append((event.xdata, event.ydata))
            else:
                col = self.cmap[len(self.pointl)]
                circ.set_color(col)
                self.ax2.add_patch(circ)
                self.pointl.append((event.xdata, event.ydata))
            self.fig.canvas.draw()

            if len(self.pointr) > 8 and len(self.pointl) > 8 and self.F is None:
                self.calculateF()
        except:
            pass

    def calculateF(self):
        self.F = 'calculate'
        log.info("Calculate F now...")
        minlen = min(self.pointl.shape[0], self.pointr.shape[0])
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
