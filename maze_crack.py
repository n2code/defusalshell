from __future__ import print_function

import re
from functools import reduce

maze_raw_data = '<?xml version="1.0" encoding="utf-16"?><svg width="100%" height="100%" viewBox="0 0 300 300" preserveAspectRatio="xMidYMid meet" version="1.1" xmlns="http://www.w3.org/2000/svg"><circle cx="25" cy="25" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="0" x2="50" y1="0" y2="0" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><line x1="0" x2="0" y1="0" y2="50" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="25" cy="75" r="3" stroke="black" fill="grey" stroke-width="1" /><circle cx="25" cy="75" r="15" stroke="black" fill="none" stroke-width="1" /><line x1="0" x2="0" y1="50" y2="100" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="25" cy="125" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="0" x2="0" y1="100" y2="150" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="25" cy="175" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="0" x2="0" y1="150" y2="200" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="25" cy="225" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="0" x2="0" y1="200" y2="250" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="25" cy="275" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="0" x2="0" y1="250" y2="300" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><line x1="0" x2="50" y1="300" y2="300" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="75" cy="25" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="50" x2="100" y1="0" y2="0" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="75" cy="75" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="50" x2="100" y1="50" y2="50" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><line x1="50" x2="50" y1="50" y2="100" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><circle cx="75" cy="125" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="50" x2="50" y1="100" y2="150" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><circle cx="75" cy="175" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="50" x2="100" y1="150" y2="150" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><line x1="50" x2="50" y1="150" y2="200" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><circle cx="75" cy="225" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="50" x2="100" y1="200" y2="200" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><circle cx="75" cy="275" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="50" x2="100" y1="250" y2="250" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><line x1="50" x2="100" y1="300" y2="300" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="125" cy="25" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="100" x2="150" y1="0" y2="0" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="125" cy="75" r="3" stroke="black" fill="grey" stroke-width="1" /><circle cx="125" cy="125" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="100" x2="150" y1="100" y2="100" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><circle cx="125" cy="175" r="3" stroke="black" fill="grey" stroke-width="1" /><circle cx="125" cy="225" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="100" x2="150" y1="200" y2="200" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><circle cx="125" cy="275" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="100" x2="100" y1="250" y2="300" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><line x1="100" x2="150" y1="300" y2="300" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="175" cy="25" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="150" x2="200" y1="0" y2="0" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><line x1="150" x2="150" y1="0" y2="50" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><circle cx="175" cy="75" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="150" x2="150" y1="50" y2="100" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><circle cx="175" cy="125" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="150" x2="200" y1="100" y2="100" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><line x1="150" x2="150" y1="100" y2="150" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><circle cx="175" cy="175" r="3" stroke="black" fill="grey" stroke-width="1" /><circle cx="175" cy="225" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="150" x2="200" y1="200" y2="200" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><line x1="150" x2="150" y1="200" y2="250" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><circle cx="175" cy="275" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="150" x2="200" y1="300" y2="300" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="225" cy="25" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="200" x2="250" y1="0" y2="0" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="225" cy="75" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="200" x2="250" y1="50" y2="50" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><circle cx="225" cy="125" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="200" x2="250" y1="100" y2="100" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><circle cx="225" cy="175" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="200" x2="250" y1="150" y2="150" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><line x1="200" x2="200" y1="150" y2="200" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><circle cx="225" cy="225" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="200" x2="250" y1="200" y2="200" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><circle cx="225" cy="275" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="200" x2="250" y1="250" y2="250" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><line x1="200" x2="200" y1="250" y2="300" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><line x1="200" x2="250" y1="300" y2="300" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="275" cy="25" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="250" x2="300" y1="0" y2="0" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><line x1="300" x2="300" y1="0" y2="50" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="275" cy="75" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="250" x2="300" y1="50" y2="50" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><line x1="300" x2="300" y1="50" y2="100" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="275" cy="125" r="3" stroke="black" fill="grey" stroke-width="1" /><circle cx="275" cy="125" r="15" stroke="black" fill="none" stroke-width="1" /><line x1="300" x2="300" y1="100" y2="150" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="275" cy="175" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="300" x2="300" y1="150" y2="200" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="275" cy="225" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="250" x2="250" y1="200" y2="250" stroke="black" stroke-width="3" stroke-dasharray="" fill="none" /><line x1="300" x2="300" y1="200" y2="250" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><circle cx="275" cy="275" r="3" stroke="black" fill="grey" stroke-width="1" /><line x1="300" x2="300" y1="250" y2="300" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /><line x1="250" x2="300" y1="300" y2="300" stroke="black" stroke-width="10" stroke-dasharray="" fill="none" /></svg>'


def to_line(x1, x2, y1, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    if min(dx, dy) == dx:
        return ((x1, y1), (x1, y2))
    else:
        return ((x1, y1), (x2, y1))


def correct(a):
    facter = 50

    def f(n):
        return int((n - (facter / 2)) / facter)

    (x, y) = a
    return (f(x), f(y))


def correctConnection(c):
    (a, b) = c
    return (correct(a), correct(b))


walls = re.findall('<line\s+x1="(\d+)"\s*x2="(\d+)"\s*y1="(\d+)"\s*y2="(\d+)"\s*stroke="black"\s*stroke-width="3"',
                   maze_raw_data)
walls = [to_line(int(x1), int(x2), int(y1), int(y2)) for (x1, x2, y1, y2) in walls]

dots = re.findall('<circle\s+cx="(\d+)"\s*cy="(\d+)" r="3"', maze_raw_data)
dots = [(int(x), int(y)) for (x, y) in dots]

circles = re.findall('<circle\s+cx="(\d+)"\s*cy="(\d+)"\s*r="15"', maze_raw_data)
circles = [correct((int(x), int(y))) for (x, y) in circles]


def strip_duplicates(adjacents):
    def add_or_ignore(acc, element):
        (a, b) = element
        return (acc + [element]) if not (b, a) in acc else acc

    return reduce(add_or_ignore, adjacents, [])


def separated_by_wall(connection):
    ((x1, y1), (x2, y2)) = connection

    if y1 == y2:
        minx = min(x1, x2)
        maxx = max(x1, x2)
        separators = [1 for ((wx1, wy1), (wx2, wy2)) in walls if
                      wx1 == wx2 and wx1 > minx and wx1 < maxx and y1 > min(wy1, wy2) and y1 < max(wy1, wy2)]
    else:
        miny = min(y1, y2)
        maxy = max(y1, y2)
        separators = [1 for ((wx1, wy1), (wx2, wy2)) in walls if
                      wy1 == wy2 and wy1 > miny and wy1 < maxy and x1 > min(wx1, wx2) and y1 < max(wx1, wx2)]

    return len(separators) > 0


def close_enough(a, b):
    (x1, y1) = a
    (x2, y2) = b
    if x1 == x2 and y1 == y2:
        return False

    if y1 == y2:
        distance = abs(x2 - x1)
    elif x1 == x2:
        distance = abs(y2 - y1)
    else:
        return False

    print(distance)
    return distance <= 50


adjacentDots = [((x1, y1), (x2, y2)) for (x1, y1) in dots for (x2, y2) in dots if close_enough((x1, y1), (x2, y2))]

validConnections = [correctConnection(x) for x in adjacentDots if not separated_by_wall(x)]


def successors(connections, node):
    return [target for (origin, target) in connections if origin == node]


def traverse(connections, start, until, seen=None):
    if not seen:
        seen = []
    if start == until:
        return [seen]

    seen = seen + [start]
    for successor in successors(connections, start):
        if not successor in seen:
            path = traverse(connections, successor, until, seen)
            if path and path[-1] == until:
                return path + [start]
    return []


print(traverse(validConnections, (3, 1), (4, 3)))
