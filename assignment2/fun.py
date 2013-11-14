import numpy as np
import scipy as sp
import scipy.linalg as l

import logging

log = logging.getLogger(__name__)

# x'Fx = 0
# (x' y' 1) [f1 f2 f3; f4 f5 f6; f7 f8 f9] (x y 1) = 0
# [x'x, x'y, x', y'x, y'y, y', x, y, 1] [f1 ... f9] = 0
# A vF = 0
#
def produce_row(p1, p2):
    """Produces restriction row for 2d points p1, p2."""
    p1 = np.array(p1)
    p2 = np.array(p2)
    p1 = p1/l.norm(p1)
    p2 = p2/l.norm(p2)
    return np.array([p1[0]*p2[0], p1[0]*p2[1], p1[0],
                    p1[1]*p2[0], p1[1]*p2[1], p1[1],
                    p2[0], p2[1], 1]) # trimmed to get unique solution

def produce_matrix(P1, P2):
    """Produces a matrix that can be solved for F"""
    log.debug("Prod matrix:")
    log.debug(len(P1))
    log.debug(P1)
    log.debug(len(P2))
    log.debug(P2)
    assert len(P1) == len(P2)
    assert len(P1) > 7
    return np.vstack([produce_row(p1, p2) for p1, p2 in zip(P1, P2)])

def rank(A, eps=1e-12):
    u, s, vh = np.linalg.svd(A)
    return len([x for x in s if abs(x) > eps])

def get_F(P1, P2):
    log.debug('produce matrix')
    A = produce_matrix(P1, P2)
    log.debug('A:\n%s', str(A))
    f = l.pinv(A)[8]
    log.debug(str(f))
    f = f/l.norm(f)
    # Ensure F does have rank 2:
    # f[8] so that
    #   0 = c f[0] + d f[3] - f[6]
    #   0 = c f[1] + d f[4] - f[7]
    #   0 = c f[2] + d f[5] - f[8]
    log.info(f.shape)
    f.shape = (3, 3)
    return f

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    P1 = ((103.96451612903223, 119.24193548387109),
          (4.041935483870958, 253.22903225806465),
          (117.59032258064514, 305.46129032258074),
          (312.89354838709676, 210.08064516129036),
          (358.31290322580645, 332.71290322580654),
          (149.38387096774193, 357.69354838709683),
          (233.40967741935481, 157.84838709677422),
          (417.35806451612899, 189.64193548387107))
    P2 = ((168.58387096774197, 119.24193548387109),
          (93.641935483870952, 250.95806451612907),
          (198.10645161290324, 307.7322580645162),
          (391.13870967741934, 205.53870967741943),
          (461.53870967741921, 332.71290322580649),
          (254.88064516129032, 362.23548387096781),
          (307.11290322580646, 166.93225806451619),
          (488.79032258064501, 189.64193548387107))
    print get_F(P1, P2)
