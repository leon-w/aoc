import sys

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    d = lines.pop(0)
    tree = {}

    for line in lines:
        node, rest = line.split(" = (")
        l, r = rest[:-1].split(", ")
        tree[node] = (l, r)

    return d, tree


def part1():
    d, tree = parse_input()

    i = 0
    node = "AAA"
    while True:
        node = tree[node][d[i % len(d)] == "R"]
        i += 1
        if node == "ZZZ":
            break

    print(i)


def part2():
    d, tree = parse_input()

    nodes = [n for n in tree.keys() if n[-1] == "A"]
    steps = []
    for node in nodes:
        i = 0
        while True:
            node = tree[node][d[i % len(d)] == "R"]
            i += 1
            if node[-1] == "Z":
                steps.append(i)
                break

    print(np.lcm.reduce(steps))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
