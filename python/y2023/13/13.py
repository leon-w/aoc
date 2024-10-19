import sys

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines()]
    lines.append("")

    puzzles = []
    puzzle = []
    for line in lines:
        if len(line) == 0:
            puzzles.append((np.array(puzzle) == "#").astype(int))
            puzzle = []
        else:
            puzzle.append(list(line))

    return puzzles


def get_axes(puzzle, thresh=0):
    for i in range(1, puzzle.shape[0]):
        size = min(i, puzzle.shape[0] - i)
        if np.count_nonzero(puzzle[i - size : i] != puzzle[i : i + size][::-1]) == thresh:
            return i
    return 0


def part1():
    data = parse_input()

    total = 0
    for puzzle in data:
        total += get_axes(puzzle.T) + 100 * get_axes(puzzle)

    print(total)


def part2():
    data = parse_input()

    total = 0
    for puzzle in data:
        total += get_axes(puzzle.T, thresh=1) + 100 * get_axes(puzzle, thresh=1)

    print(total)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
