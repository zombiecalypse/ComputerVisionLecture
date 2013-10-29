import albedo
import chrome_sphere
import depth

from scipy.misc import imread, imshow
from scipy import linalg as l
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.cm as cm

import sys
import logging

log = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s::%(name)s::%(levelname)s:\t%(message)s')
logging.basicConfig(level=logging.INFO, formatter=formatter)


template = '../Images/{0}/{0}.{1}.png'

lights = chrome_sphere.run()

for name in ['buddha', 'cat', 'gray', 'horse', 'owl', 'rock']:
    log.info('Processing %s', name)

    mask = imread(template.format(name, 'mask'), True)
    mask3 = np.array([mask, mask, mask]).transpose([1,2,0])
    images = []
    for i in range(12):
        filename = template.format(name, i)
        images.append(imread(filename))
    imgs = np.array(images)

    n_tilde = albedo.extract_n_tilde(lights, imgs)

    al, n = albedo.albedo_normals(n_tilde)

    n = n.transpose([1,2,0])

    z = depth.depths(mask, n)

    plt.subplot(2,2,1)
    plt.imshow(al)

    plt.subplot(2,2,2)
    plt.imshow(np.abs(n))

    plt.subplot(2,2,3)
    plt.imshow(z, cmap = cm.Greys_r)

    plt.subplot(2,2,4)
    plt.hist(z.flatten(), 300, range=(0.05,1.10), fc='k', ec='k')

    plt.savefig('../out/{0}.png'.format(name))
