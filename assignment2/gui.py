import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg


def onclick(event):
    print 'x=%f, y=%f %s'%(event.xdata, event.ydata, event.inaxes)

if __name__ == '__main__':
    import sys
    fig = plt.figure()

    imgl = mpimg.imread(sys.argv[1])
    imgr = mpimg.imread(sys.argv[2])

    ax1 = fig.add_subplot(1, 2, 0, axes=None)
    plt.imshow(imgl)
    ax1.figure.canvas.mpl_connect('button_press_event', onclick)

    ax2 = fig.add_subplot(1, 2, 1, frame_on=False)
    plt.imshow(imgr)

    plt.show()
