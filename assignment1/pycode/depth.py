from scipy.sparse import dok_matrix
from scipy.sparse.linalg import lsqr
import numpy as np
import logging
log = logging.getLogger(__name__)

Y,X,Z = 0,1,2

def normalize(z):
    b,t = np.percentile(z, [5,95])
    return (z-b)/(t-b)

class ConsistentBimap(object):
    def __init__(self):
        self._map = dict()
        self._imap = dict()
        self.i = 0

    def __getitem__(self, i):
        if i not in self._map: 
            self._map[i] = self.i
            self._imap[self.i] = i
            self.i += 1
        return self._map[i]

    def values(self):
        return self._map.values()

    @property
    def r(self):
        return self._imap


def depths(mask, normals):
    """Reconstructs the depths from normals.
    
    Args:
        normals: width x height x 3 array
    """
    width, height, three = normals.shape
    assert three == 3
    m = dok_matrix((width*height*2, width*height), dtype=float)
    b = np.zeros(width*height*2, dtype=float)
    log.debug('maximal shape: %s', m.shape)
    row = 0
    coords = ConsistentBimap()
    for x in range(width):
        for y in range(height):
            if not mask[x,y]: continue
            elif not (mask[x+1,y] and mask[x,y+1] and mask[x-1,y] and mask[x,y-1]):
                continue
                # set border to zero
                m[row, coords[(x,y)]] = 1
                b[row] = 0
                row += 1
            else:
                # n_z (z(x+1, y) - z(x, y)) = -n_x
                m[row, coords[(x+1,y)]] = 1
                m[row, coords[(x,y)]] = -1
                b[row] = normals[x,y,X]/normals[x,y,Z]
                row += 1

                # n_z (z(x, y+1) - z(x, y)) = -n_y
                m[row, coords[(x,y+1)]] = 1
                m[row, coords[(x,y)]] = -1
                b[row] = normals[x,y,Y]/normals[x,y,Z]
                row += 1

    # Now we know how many pixels are used and we restrict the matrix to the
    # rows needed.
    m_p = dok_matrix((row+1, coords.i), dtype=float)

    for (x,y), v in m.items():
        try:
            m_p[x,y] = v
        except Exception as e:
            log.error('error at (%s, %s)', x, y)
            raise
    # normalization
    m_p[row,0] = 1
    m_p = m_p.tocsr()
    b = b[:row+1]
    log.debug('actual shape: %s', m_p.shape)
    s = lsqr(m_p, b, atol=1e-3, btol=1e-6, show=True)
    z_p = s[0]
    z_p = normalize(z_p)
    z = np.zeros((width, height))
    for row,(x,y) in coords.r.items():
        z[x,y] = z_p[row]
    log.debug('z(0,0) = %s', z[0,0])
    return z
