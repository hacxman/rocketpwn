import math
import random

def get_tile_pair_pos(tile, lvl, tiles):
    pairs = []
    for y in range(len(lvl)):
        for x in range(len(lvl[y])):
            if lvl[x][y] == tile.lower():
                pairs.append((x, y))
    p = pairs[random.randrange(0, len(pairs))]
    for t in tiles:
        if t.coords == p:
            return t.rect

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
