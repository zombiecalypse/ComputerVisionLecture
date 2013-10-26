import albedo
import chrome_sphere
import depth

from scipy.misc import imread, imshow
from scipy import linalg as l
import matplotlib.pyplot as plt
import numpy as np

import sys
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
depth.log.setLevel(logging.INFO)


template = '../Images/{0}/{0}.{1}.png'
name = sys.argv[1]

mask = imread(template.format(name, 'mask'), True)
mask3 = np.array([mask, mask, mask]).transpose([1,2,0])
imgs = []
for i in range(12):
    filename = template.format(name, i)
    imgs.append(imread(filename))
imgs = np.array(imgs)
log.info(imgs.shape)
n_tilde = albedo.extract_n_tilde(chrome_sphere.example, imgs)
al, n = albedo.albedo_normals(n_tilde)
n = n.transpose([1,2,0])

z = depth.depths(mask, n)
log.info('shape: %s min: %s max: %s', z.shape, z.min(), z.max())

plt.subplot(2,1,1)
plt.imshow(al)

plt.subplot(2,1,2)
plt.imshow(np.abs(n))

plt.subplot(2,2,1)
plt.imshow(np.abs(z))

plt.show()
