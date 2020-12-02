import numpy as np
import math

#### This file contains simple functions to compute bezier and line curve points, given the control points

# Determine curve type
def curve_is_line(ctrl_pts):
    return (len(ctrl_pts) > 0 and len(ctrl_pts[0]) == 2)

#### POLY BEZIER UTILITIES

def binomial(i, n):
    """Binomial coefficient"""
    return math.factorial(n) / float(
        math.factorial(i) * math.factorial(n - i))


def bernstein(t, i, n):
    """Bernstein polynom"""
    return binomial(i, n) * (t ** i) * ((1 - t) ** (n - i))


def bezier(t, points):
    """Calculate coordinate of a point in the bezier curve"""
    n = len(points) - 1
    x = y = z = 0
    for i, pos in enumerate(points):
        bern = bernstein(t, i, n)
        x += pos[0] * bern
        y += pos[1] * bern
        z += pos[2] * bern
    return x, y, z

def get_idx_and_param(t, beziers):
    n = len(beziers)
    if t == 1:
        return (n - 1, 1)

    p = [(i/n) for i in range(n + 1)]
    bezier_idx = int(t * n)
    u = (t - p[bezier_idx]) / (p[bezier_idx + 1] - p[bezier_idx])
    return (bezier_idx, u)

def poly_bezier(ts, beziers):
    idx_params = [get_idx_and_param(ti, beziers) for ti in ts]
    points = np.array([bezier(idx_params[i][1], beziers[idx_params[i][0]])
                       for i in range(len(idx_params))])
    return points[:, 0], points[:, 1], points[:, 2]

def poly_bezier_t(t, beziers):
    idx, u = get_idx_and_param(t, beziers)
    return np.array(bezier(u, beziers[idx]))


#### LINE UTILITIES (by default this supports poly-lines defined as lists of lines)
## A line from p to q is simply: [[p, q]]

def poly_line_t(t, ctrl_pts):
    idx, u = get_idx_and_param(t, ctrl_pts)
    return line_t(u, ctrl_pts[idx])

def line_t(t, ctrl_pts):
    A = np.array(ctrl_pts[0])
    B = np.array(ctrl_pts[1])
    return A + (B-A) * t