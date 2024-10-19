import itertools
import sys

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    data = [[0 if c == "." else 1 for c in row] for row in lines]

    return np.array(data)


def expand(data, factor):
    rows = data.sum(axis=1) == 0
    cols = data.sum(axis=0) == 0

    gy, gx = np.nonzero(data)

    for i, y in enumerate(gy):
        gy[i] += rows[:y].sum() * (factor - 1)

    for i, x in enumerate(gx):
        gx[i] += cols[:x].sum() * (factor - 1)

    return gy, gx


def part1():
    data = parse_input()

    gy, gx = expand(data, factor=2)

    dist = 0
    for a, b in itertools.combinations(range(len(gy)), 2):
        dist += abs(gy[a] - gy[b]) + abs(gx[a] - gx[b])

    print(dist)


def part2():
    data = parse_input()

    gy, gx = expand(data, factor=1000000)

    dist = 0
    for a, b in itertools.combinations(range(len(gy)), 2):
        dist += abs(gy[a] - gy[b]) + abs(gx[a] - gx[b])

    print(dist)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
