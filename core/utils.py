import math


def rot_point(point, pivot, angle):
    rads = math.radians(angle)
    s = math.sin(rads)
    c = math.cos(rads)

    x = point[0] - pivot[0]
    y = point[1] - pivot[1]

    nx = x * c - y * s
    ny = x * s + y * c

    return (nx + pivot[0], ny + pivot[1])


def scale(x, a, b, l=0., h=1.):
    return ((h - l) * (x - b)) / (a - b) + l
