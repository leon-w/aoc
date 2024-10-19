import re
import sys
from collections import defaultdict


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    return lines


def compute_maximum_path_length(island_map):
    w = len(island_map[0])
    h = len(island_map)
    ds_all = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    start = (1, 0)
    end = (w - 2, h - 1)
    nodes = set([start, end])

    # identify nodes (crossroads)
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if island_map[y][x] == "#":
                continue
            if sum(island_map[y + dy][x + dx] != "#" for dy, dx in ds_all) != 2:
                nodes.add((x, y))

    distances = defaultdict(list)

    # calculate distances between nodes
    for node in nodes:
        q = [(node, 0)]
        visited = set()
        while len(q) > 0:
            (x, y), dist = q.pop(0)
            visited.add((x, y))

            match island_map[y][x]:
                case "^":
                    ds = [(0, -1)]
                case "v":
                    ds = [(0, 1)]
                case "<":
                    ds = [(-1, 0)]
                case ">":
                    ds = [(1, 0)]
                case _:
                    ds = ds_all

            for dx, dy in ds:
                if 0 <= x + dx < w and 0 <= y + dy < h and island_map[y + dy][x + dx] != "#":
                    new_pos = (x + dx, y + dy)
                    if new_pos in visited:
                        continue

                    if new_pos in nodes:
                        distances[node].append((new_pos, dist + 1))
                        continue

                    q.append((new_pos, dist + 1))

    # find longest path
    q = [(start, 0, {start})]
    max_dist = 0

    while len(q) > 0:
        node, dist, visited = q.pop()

        if node == end:
            max_dist = max(max_dist, dist)
            continue

        for n, n_dist in distances[node]:
            if n not in visited:
                q.append((n, dist + n_dist, visited | {n}))

    return max_dist


def part1():
    island_map = parse_input()

    print(compute_maximum_path_length(island_map))


def part2():
    island_map = parse_input()

    island_map = [re.sub(r"[\^v<>]", ".", l) for l in island_map]

    print(compute_maximum_path_length(island_map))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
