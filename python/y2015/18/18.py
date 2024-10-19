import sys

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    mapping = {".": 0, "#": 1}
    return np.array([[mapping[c] for c in line] for line in lines], dtype=np.int8)


def simulate(grid, iterations, corners_on=False):
    def set_corners():
        for pos in [(0, 0), (-1, 0), (0, -1), (-1, -1)]:
            grid[pos] = 1

    shape_array = np.array(grid.shape)

    if corners_on:
        set_corners()

    for _ in range(iterations):
        new_grid = np.zeros_like(grid)
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                pos = np.array([y, x])
                a = np.clip(pos - 1, 0, shape_array)
                b = np.clip(pos + 2, 0, shape_array)
                cell = grid[y, x]
                n = grid[a[0] : b[0], a[1] : b[1]].sum() - cell

                if cell:
                    new_grid[y, x] = 2 <= n <= 3
                else:
                    new_grid[y, x] = n == 3

        grid = new_grid

        if corners_on:
            set_corners()

    return grid.sum()


def part1():
    grid = parse_input()

    print(simulate(grid, 100))


def part2():
    grid = parse_input()

    print(simulate(grid, 100, corners_on=True))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
