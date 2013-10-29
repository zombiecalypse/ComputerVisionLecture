import albedo
import chrome_sphere
import depth

from scipy.misc import imread, imshow
from scipy import linalg as l
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

import matplotlib.cm as cm

import sys
import logging

log = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s::%(name)s::%(levelname)s:\t%(message)s')
logging.basicConfig(level=logging.INFO, formatter=formatter)


template = '../Images/{0}/{0}.{1}.png'

lights = chrome_sphere.example

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

    plt.subplot(1,3,1)
    plt.imshow(images[0])
    plt.title("Image")

    plt.subplot(1,3,2)
    plt.imshow(np.abs(n))
    plt.title("Normals")

    plt.subplot(1,3,3)
    plt.imshow(al)
    plt.title("Albedo")
    plt.savefig('../out/{0}_normals.png'.format(name), bbox_inches='tight', pad_inches=0)

    plt.figure()
    gs = gridspec.GridSpec(1, 3, height_ratios=[1, 1, 1]) 
    ax=plt.subplot(gs[0])
    #ax.title("Image")
    ax.imshow(images[0])

    ax=plt.subplot(gs[1])
    #ax.title("Depth")
    ax.imshow(z, cmap = cm.Greys_r)

    ax=plt.subplot(gs[2])
    #ax.title("Histogram of Depth")
    ax.hist(z.flatten(), 300, range=(0.05,1.10), fc='k', ec='k')

    plt.savefig('../out/{0}_depth.png'.format(name), bbox_inches='tight', pad_inches=0)
