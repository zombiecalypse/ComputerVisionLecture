# coding=utf8
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
    x_p, y_p = p1[0], p1[1]
    x,   y   = p2[0], p2[1]
    return np.array([
            x_p*x, x_p*y, x_p,
            y_p*x, y_p*y, y_p,
            x, y, 1])

# mean(T⁻¹ X) = 0
# std(T⁻¹ X)² = 2
def normalized(P):
    mu = P.mean(axis=0)
    delta = P - mu
    sig = np.sqrt((delta**2).sum(axis=1)).mean()
    log.debug("mu: %s sig: %s", mu, sig)
    T = np.eye(3,3)
    # Normalize for std deviation
    sig_target = 2/sig
    T[0,0] *= sig_target
    T[1,1] *= sig_target
    # Normalize for mean
    T[0:2, 2] = -mu*sig_target
    Pp = np.hstack([P, np.array([[1]]*P.shape[0])])
    Q = l.solve(T, Pp.T).T

    # Check functionality: OK
    log.debug("%s vs %s", T.shape, Pp.shape)
    log.debug("%s", np.dot(T, np.array([mu[0], mu[1], 1])))
    P_p = np.dot(T, Pp.T).T
    mu_p = P_p.mean(axis=0)
    delta_p = P_p - mu_p
    sig_p = np.sqrt((delta_p**2).sum(axis=1)).mean()
    log.debug("mu': %s sig: %s", mu_p, sig_p)
    return Q, T

def produce_matrix(P1, P2):
    """Produces a matrix that can be solved for F"""
    assert len(P1) == len(P2)
    assert len(P1) > 7
    P1 = np.array(P1)
    P2 = np.array(P2)
    P1, T1 = normalized(P1)
    P2, T2 = normalized(P2)
    return np.vstack([produce_row(p1, p2) for p1, p2 in zip(P1, P2)]), T1, T2

def rank(A, eps=1e-12):
    u, s, vh = np.linalg.svd(A)
    return len([x for x in s if abs(x) > eps])

def enforce_rank2(M):
    u, s, vh = np.linalg.svd(M)
    s[2] = 0
    return np.dot(u, np.dot(np.diag(s), vh))

def dot(*args):
    return reduce(np.dot, args)

def get_F(P1, P2):
    A, T1, T2 = produce_matrix(P1, P2)
    u, s, vh = np.linalg.svd(A)
    f = vh[8]
    f.shape = (3,3)
    f = enforce_rank2(f)
    f = dot(T2.T, f, T1)
    # Check functionality: OK
    log.debug('rank: %s', rank(f))
    for i, (p1, p2) in enumerate(zip(P1, P2)):
        p1 = dot(T1, np.append(p1, 1))
        p2 = dot(T2, np.append(p2, 1))
        # Product should be 1:
        # p1 perp to p2, except for last component, which is 1 for both
        log.debug('%8s: %s', i, dot(p2.T, f, p1)-1)
    return f

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    P1 = ((103.96451612903223, 119.24193548387109),
          (4.041935483870958,  253.22903225806465),
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
