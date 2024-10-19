import sys

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [list(l.strip()) for l in f.readlines() if l.strip()]

    char_map = {
        ".": 0,
        "O": 1,
        "#": 2,
    }

    # for some reason, int64 is a lot faster than other types
    grid = np.array([[char_map[c] for c in row] for row in lines], dtype=np.int64)

    return grid


def move_up(grid):
    for y in range(1, grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 1:
                last_valid_i = None
                for i in range(y - 1, -1, -1):
                    if grid[i, x] == 0:
                        last_valid_i = i
                    else:
                        break
                if last_valid_i is not None:
                    grid[y, x] = 0
                    grid[last_valid_i, x] = 1


def compute_load(grid):
    load = 0
    for i, row in enumerate(grid):
        rocks = np.count_nonzero(row == 1)
        load += rocks * (grid.shape[0] - i)
    return load


def part1():
    grid = parse_input()

    move_up(grid)
    load = compute_load(grid)

    print(load)


def part2():
    grid = parse_input()

    cycles = 1000000000

    known_hashes = {}
    loop = None
    last_load = None
    for i in range(cycles):
        h = hash(grid.data.tobytes())
        last_load = compute_load(grid)
        if h in known_hashes:
            loop = (known_hashes[h][0], i)
            break
        known_hashes[h] = (i, last_load)

        # a single cycle
        for _ in range(4):
            move_up(grid)
            grid = np.rot90(grid, k=-1)

    if loop is not None:
        start, end = loop
        loop_len = end - start
        i = ((cycles - start) % loop_len) + start
        for ii, load in known_hashes.values():
            if i == ii:
                print(load)
                break
    else:
        print(last_load)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
