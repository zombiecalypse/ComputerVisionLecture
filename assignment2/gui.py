import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import CirclePolygon


class StereoVision(object):
    def __init__(self, l, r):
        self.imgl = mpimg.imread(l)
        self.imgr = mpimg.imread(r)
        self.fig = plt.figure()

    def onclick(self, event):
        r = self.resolve(event.inaxes)
        print 'x=%f, y=%f %s'%(event.xdata, event.ydata, r)

        circ = CirclePolygon((event.xdata, event.ydata), 5, color='r')
        if r == 'r':
            self.ax1.add_patch(circ)
        else:
            self.ax2.add_patch(circ)
        self.fig.canvas.draw()

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
