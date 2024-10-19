import sys

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    return lines


class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vec({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))


# origin is in the top left
UP = Vec(0, -1)
LEFT = Vec(-1, 0)
DOWN = Vec(0, 1)
RIGHT = Vec(1, 0)
directions = [UP, LEFT, DOWN, RIGHT]

direction_map = {
    "|": [UP, DOWN],
    "-": [LEFT, RIGHT],
    "L": [UP, RIGHT],
    "J": [UP, LEFT],
    "7": [LEFT, DOWN],
    "F": [RIGHT, DOWN],
}

left_side_map = {
    "|": [RIGHT],
    "-": [UP],
    "L": [],
    "J": [RIGHT, DOWN],
    "7": [UP, RIGHT],
    "F": [],
}

right_side_map = {
    "|": [LEFT],
    "-": [DOWN],
    "L": [DOWN, LEFT],
    "J": [],
    "7": [],
    "F": [UP, LEFT],
}

opposite_map = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}


def find_start_pos(data):
    # find s
    x, y = 0, 0
    for y, row in enumerate(data):
        if "S" in row:
            x = row.index("S")
            break

    pos = Vec(x, y)
    connecting_points = set()

    # find starting position
    for d in directions:
        new_pos = pos + d
        c = data[new_pos.y][new_pos.x]
        if c in direction_map:
            if opposite_map[d] in direction_map[c]:
                connecting_points.add(d)

    # determine the pipe type below s
    s_letter = "S"
    for c, conns in direction_map.items():
        if set(conns) == connecting_points:
            s_letter = c
            break

    return pos, s_letter


def part1():
    data = parse_input()

    s_pos, s_c = find_start_pos(data)

    steps = 1
    pos = s_pos
    current_d = direction_map[s_c][0]
    while True:
        c = data[pos.y][pos.x]
        if c == "S":
            c = s_c

        d1, d2 = direction_map[c]
        current_d = d2 if opposite_map[d1] == current_d else d1
        pos = pos + current_d
        steps += 1

        if pos == s_pos:
            break

    print(steps // 2)


def part2():
    data = parse_input()
    grid = np.zeros((len(data), len(data[0])), dtype=int)

    def is_valid_pos(pos):
        return pos.x >= 0 and pos.x < len(grid[0]) and pos.y >= 0 and pos.y < len(grid)

    # def print_grid():
    #     cmap = {
    #         0: " ",
    #         1: "#",
    #         2: ".",
    #     }
    #     border = "+" + "-" * len(grid[0]) + "+"
    #     print(border)
    #     for row in grid:
    #         print("|" + "".join(cmap[c] for c in row) + "|")
    #     print(border)

    s_pos, s_c = find_start_pos(data)

    # follow loop and mark one side of the path
    pos = s_pos
    current_d = direction_map[s_c][0]
    while True:
        c = data[pos.y][pos.x]
        if c == "S":
            c = s_c

        grid[pos.y, pos.x] = 1

        d1, d2 = direction_map[c]
        reverse = opposite_map[d1] == current_d

        for side_d in (right_side_map if reverse else left_side_map)[c]:
            side_pos = pos + side_d
            if is_valid_pos(side_pos) and grid[side_pos.y, side_pos.x] == 0:
                grid[side_pos.y, side_pos.x] = 2

        current_d = d2 if reverse else d1
        pos = pos + current_d

        if pos == s_pos:
            break

    side_pos_queue = []
    for y, x in zip(*np.nonzero(grid == 2)):
        side_pos_queue.append(Vec(x, y))

    # grow area
    while side_pos_queue:
        side_pos = side_pos_queue.pop()
        for d in directions:
            new_side_pos = side_pos + d
            if is_valid_pos(new_side_pos) and grid[new_side_pos.y, new_side_pos.x] == 0:
                grid[new_side_pos.y, new_side_pos.x] = 2
                side_pos_queue.append(new_side_pos)

    area1 = (grid == 2).sum()
    area2 = (grid == 0).sum()

    print(f"Area 1: {area1}    Area 2: {area2}")


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
