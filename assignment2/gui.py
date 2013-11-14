import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import CirclePolygon

import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import fun
fun.log.level = logging.INFO


class StereoVision(object):
    def __init__(self, l, r):
        self.imgl = mpimg.imread(l)
        self.imgr = mpimg.imread(r)
        self.fig = plt.figure()
        self.pointl = []
        self.pointr = []

    def onclick(self, event):
        r = self.resolve(event.inaxes)
        try:
            log.debug('x=%f, y=%f %s'%(event.xdata, event.ydata, r))

            circ = CirclePolygon((event.xdata, event.ydata), 5, color='r',
                                 alpha=0.75)
            if r == 'r':
                self.ax1.add_patch(circ)
                self.pointr.append((event.xdata, event.ydata))
            else:
                self.ax2.add_patch(circ)
                self.pointl.append((event.xdata, event.ydata))
            self.fig.canvas.draw()

            if len(self.pointr) > 8 and len(self.pointl) > 8:
                log.info("Calculate F now...")
                F = self.calculateF()
                log.info("done...")
                log.info("F: %s", F)
        except:
            pass

    def calculateF(self):
        return fun.get_F(tuple(self.pointl[:9]), tuple(self.pointr[:9]))

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
