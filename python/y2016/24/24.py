import itertools
import sys

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    marker = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c.isdigit():
                marker[c] = (x, y)

    vents = np.array([[c == "#" for c in line] for line in lines])

    return marker, vents


def find_shortest_sequence(marker, vents, end_at_start):
    def find_shortest_distance(start, end):
        vents_map = vents.copy()
        h, w = vents.shape

        q = [(*start, 0)]
        t = 0
        while len(q):
            t += 1
            x_c, y_c, d = q.pop(0)

            if (x_c, y_c) == end:
                return d

            if vents_map[y_c, x_c]:
                continue

            vents_map[y_c, x_c] = True

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                x_n = x_c + dx
                y_n = y_c + dy

                if x_n >= 0 and x_n < w and y_n >= 0 and y_n < h and not vents_map[y_n, x_n]:
                    q.append((x_n, y_n, d + 1))
        return -1

    distances = {}

    for a, b in itertools.combinations(marker.keys(), 2):
        distances[(a, b)] = distances[(b, a)] = find_shortest_distance(marker[a], marker[b])

    min_d = float("inf")
    for order in itertools.permutations(m for m in marker.keys() if m != "0"):
        d = 0
        station = "0"
        if end_at_start:
            order = order + ("0",)
        for next_station in order:
            d += distances[(station, next_station)]
            station = next_station
            if d > min_d:
                break
        min_d = min(min_d, d)

    return min_d


def part1():
    marker, vents = parse_input()

    print(find_shortest_sequence(marker, vents, False))


def part2():
    marker, vents = parse_input()

    print(find_shortest_sequence(marker, vents, True))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
