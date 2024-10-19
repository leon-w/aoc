import itertools
import sys
from collections import defaultdict


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    happiness_map = defaultdict(dict)

    for line in lines:
        parts = line.split(" ")
        a = parts[0]
        b = parts[-1][:-1]
        v = int(parts[3])
        factor = -1 if parts[2] == "lose" else 1

        happiness_map[a][b] = factor * v

    return happiness_map


def happiness_scores(happiness_map):
    for order in itertools.permutations(happiness_map.keys()):
        happiness = 0
        for i in range(len(order)):
            happiness += happiness_map[order[i]][order[(i + 1) % len(order)]]
            happiness += happiness_map[order[i]][order[(i - 1) % len(order)]]
        yield happiness


def part1():
    happiness_map = parse_input()

    print(max(happiness_scores(happiness_map)))


def part2():
    happiness_map = parse_input()

    for v in happiness_map.values():
        v["Me"] = 0
    happiness_map["Me"] = {k: 0 for k in happiness_map.keys()}

    print(max(happiness_scores(happiness_map)))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
