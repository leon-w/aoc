import sys

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    def parse_coord(s):
        x, y = map(int, s.split(","))
        return x, y

    instructions = []
    for line in lines:
        variant, c1, _, c2 = line.rsplit(" ", maxsplit=3)
        instructions.append((variant, parse_coord(c1), parse_coord(c2)))

    return instructions


def part1():
    instructions = parse_input()

    grid = np.zeros((1000, 1000), dtype=np.bool_)

    for variant, (x1, y1), (x2, y2) in instructions:
        area = grid[y1 : y2 + 1, x1 : x2 + 1]
        match variant:
            case "turn on":
                area[:] = True
            case "turn off":
                area[:] = False
            case "toggle":
                area[:] = ~area[:]

    print(np.count_nonzero(grid))


def part2():
    instructions = parse_input()

    grid = np.zeros((1000, 1000), dtype=np.int64)

    for variant, (x1, y1), (x2, y2) in instructions:
        area = grid[y1 : y2 + 1, x1 : x2 + 1]
        match variant:
            case "turn on":
                area[:] += 1
            case "turn off":
                area[:] = np.clip(area - 1, 0, None)
            case "toggle":
                area[:] += 2

    print(grid.sum())


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
