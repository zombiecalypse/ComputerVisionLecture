from numpy.linalg import lstsq as least_square
import numpy as np
import logging
log = logging.getLogger(__name__)

def extract_n_tilde(lights, images):
    """Compute colour of pixel.
    
    Args:
        lights: 3 x nimages
        images: nimages x width x height array
    """
    nimages, width, height, colors = images.shape
    assert lights.shape == (nimages, 3)
    # Make a vector out of the image
    images.shape = (nimages, -1,)

    sol = least_square(lights, images)[0]
    sol.shape = (3, width, height, colors)
    return sol

def albedo_normals(n_tilde):
    norms = np.sqrt(np.sum(n_tilde ** 2, axis=0))
    albedo = norms.view()
    grey_bedo = np.mean(norms, axis=2)
    grey = np.mean(n_tilde, axis=3)
    log.info('grey_bedo: %s', grey_bedo.shape)
    log.info('grey:      %s', grey.shape)
    log.info('grey[0]:   %s', grey[0].shape)
    normals = np.nan_to_num(np.array([grey[i]/grey_bedo for i in range(3)]))
    min = albedo.min()
    max = albedo.max()
    albedo = (albedo-min)/(max-min)
    return albedo, normals
