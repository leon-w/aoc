import sys

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    d_map = {"0": "R", "1": "D", "2": "L", "3": "U"}

    instructions1 = []
    instructions2 = []

    for line in lines:
        d, l, color = line.split(" ")
        instructions1.append((d, int(l)))

        d = d_map[color[-2]]
        l = color[2:-2]
        instructions2.append((d, int(l, base=16)))

    return instructions1, instructions2


UP = np.array([-1, 0], dtype=np.int32)
DOWN = np.array([1, 0], dtype=np.int32)
LEFT = np.array([0, -1], dtype=np.int32)
RIGHT = np.array([0, 1], dtype=np.int32)
direction_map = {"U": UP, "D": DOWN, "L": LEFT, "R": RIGHT}
inside_map = {"U": RIGHT, "D": LEFT, "L": UP, "R": DOWN}


def part1():
    # naive implementation: build the polygon, fill it and measure area
    instructions, _ = parse_input()

    pos = np.array([0, 0], dtype=np.int32)
    perimeter = [pos]
    perimeter_side = []
    for d, l in instructions:
        v = direction_map[d]
        for _ in range(l):
            pos = pos + v
            perimeter.append(pos)
            perimeter_side.append(pos + inside_map[d])

    coords = np.array(perimeter + perimeter_side)
    coords -= coords.min(axis=0)
    max_x, max_y = coords.max(axis=0)

    grid = np.zeros((max_x + 1, max_y + 1), dtype=np.int8)
    grid[tuple(coords[: len(perimeter)].T)] = 1

    queue = list(coords[len(perimeter) :])
    while len(queue):
        pos = queue.pop()
        if 0 < pos[0] < max_x and 0 < pos[1] < max_y:
            if grid[tuple(pos)] != 0:
                continue
            grid[tuple(pos)] = 1
            for d in [UP, DOWN, LEFT, RIGHT]:
                queue.append(pos + d)

    print(grid.sum())


def area_polygon(points):
    return abs(np.cross(points, np.roll(points, -1, 0)).sum() // 2)


def part2():
    # faster version: compute area of polygon directly
    _, instructions = parse_input()

    pos = np.array([0, 0], dtype=np.int64)
    points = [pos]
    border = 0
    for d, l in instructions:
        v = direction_map[d]
        pos = pos + l * v
        points.append(pos)
        border += l

    area = area_polygon(points) + border // 2 + 1
    print(area)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
