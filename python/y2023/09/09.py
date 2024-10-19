import sys

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    numbers = []
    for line in lines:
        numbers.append(list(map(int, line.split())))

    return numbers


def part1():
    data = parse_input()

    results = []
    for row in data:
        last_val = row[-1]
        row = np.array(row)

        while True:
            diff = np.diff(row)
            last_val += diff[-1]

            if np.all(diff == diff[0]):
                results.append(last_val)
                break

            row = diff

    print(sum(results))


def part2():
    data = parse_input()

    results = []
    for row in data:
        row = np.array(row)

        last_vals = [row[0]]
        while True:
            diff = np.diff(row)
            last_vals.append(diff[0])

            if np.all(diff == diff[0]):
                result = last_vals[-1]
                for i in range(len(last_vals) - 2, -1, -1):
                    result = last_vals[i] - result
                results.append(result)
                break

            row = diff

    print(sum(results))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
