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


UP = Vec(0, -1)
LEFT = Vec(-1, 0)
DOWN = Vec(0, 1)
RIGHT = Vec(1, 0)

d_mapping_slash = {RIGHT: UP, DOWN: LEFT, LEFT: DOWN, UP: RIGHT}
d_mapping_backslash = {RIGHT: DOWN, DOWN: RIGHT, UP: LEFT, LEFT: UP}


def compute_number_of_energized_tiles(grid, start_head):
    energized = np.zeros((len(grid), len(grid[0])), dtype=np.int8)

    heads = [start_head]
    known_heads = set()
    while len(heads) > 0:
        pos, d = heads.pop()

        while True:
            # if out of bounds, break
            if pos.x < 0 or pos.x >= len(grid[0]) or pos.y < 0 or pos.y >= len(grid):
                break

            head = (pos, d)
            if head in known_heads:
                break
            known_heads.add(head)

            energized[pos.y, pos.x] = 1
            c = grid[pos.y][pos.x]

            if c == "-":
                if d == UP or d == DOWN:
                    heads.append((pos + LEFT, LEFT))
                    d = RIGHT
            elif c == "|":
                if d == LEFT or d == RIGHT:
                    heads.append((pos + UP, UP))
                    d = DOWN
            elif c == "/":
                d = d_mapping_slash[d]
            elif c == "\\":
                d = d_mapping_backslash[d]

            pos = pos + d

    return energized.sum()


def part1():
    grid = parse_input()

    num_tiles = compute_number_of_energized_tiles(grid, (Vec(0, 0), RIGHT))

    print(num_tiles)


def part2():
    grid = parse_input()

    possible_heads = []
    for y in range(len(grid)):
        possible_heads.append((Vec(0, y), RIGHT))
        possible_heads.append((Vec(len(grid[0]) - 1, y), LEFT))
    for x in range(len(grid[0])):
        possible_heads.append((Vec(x, 0), DOWN))
        possible_heads.append((Vec(x, len(grid) - 1), UP))

    max_num_tiles = max(compute_number_of_energized_tiles(grid, head) for head in possible_heads)

    print(max_num_tiles)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
