from scipy.sparse import dok_matrix
from scipy.sparse.linalg import lsqr
import numpy as np
import logging
log = logging.getLogger(__name__)

X,Y,Z = 0,1,2

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
    m = dok_matrix((width*height*2, width*height), dtype=float)
    b = np.zeros(width*height*2, dtype=float)
    log.info('expected shape: %s', m.shape)
    row = 0
    coords = ConsistentBimap()
    for x in range(width-1):
        for y in range(height-1):
            if not (mask[x,y] and mask[x+1,y] and mask[x+1,y]): continue
            try:
                # n_z (z(x+1, y) - z(x, y)) = -n_x
                m[row, coords[(x+1,y)]] = normals[x,y,Z]
                m[row, coords[(x,y)]] = -normals[x,y,Z]
                b[row] = -normals[x,y,X]
                row += 1

                # n_z (z(x, y+1) - z(x, y)) = -n_y
                m[row, coords[(x,y+1)]] = normals[x,y,Z]
                m[row, coords[(x,y)]] = -normals[x,y,Z]
                b[row] = -normals[x,y,Y]
                row += 1
            except Exception as e:
                logging.error('error at (%s, %s)', x, y)
                logging.error('row:    %s', row)
                logging.error('index1: %s', (x+1)+width*y)
                logging.error('index2: %s', x+width*y)
                logging.error('index3: %s', x+width*(y+1))
                logging.error('index4: %s', x+width*y)
                raise

    # Now we know how many pixels are used
    m_p = dok_matrix((row+1, coords.i), dtype=float)
    log.info('range of indices: %s to %s', 
             min(coords.values()),
             max(coords.values()))
    log.info('number of points: %s', len(coords._map))
    log.info('number of rows:   %s', row)
    log.info('max:    x:%s y:%s',
             max(k for k,_ in m.keys()),
             max(k for _,k in m.keys()))
    for (x,y), v in m.items():
        try:
            m_p[x,y] = v
        except Exception as e:
            log.error('error at (%s, %s)', x, y)
            raise
    #m_p[row,0] = 1
    m_p = m_p.tocsr()
    b = b[:row+1]
    log.info('actual shape: %s', m_p.shape)
    z_p = lsqr(m_p, b)[0]
    z = np.zeros((width, height))
    for row,(x,y) in coords.r.items():
        z[x,y] = z_p[row]
    z.shape = (width, height)
    z = (z-z.min())/(z.max()-z.min())
    return z
