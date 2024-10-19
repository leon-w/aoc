import sys

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    parse = lambda x: tuple(map(int, x.split(",")))

    slabs = []
    for line in lines:
        start, end = line.split("~")
        slabs.append((parse(start), parse(end)))

    return slabs


def compute_connections(slabs):
    slabs.sort(key=lambda s: s[0][2])

    max_x = max(s[1][0] for s in slabs)
    max_y = max(s[1][1] for s in slabs)

    height_map = np.zeros((max_x + 1, max_y + 1), dtype=np.int32)
    slab_map = np.zeros((max_x + 1, max_y + 1), dtype=np.int32)

    connections_up = {}
    connections_down = {}

    for i, slab in enumerate(slabs):
        connections_up[i + 1] = set()
        connections_down[i + 1] = set()

        slab_pos = (slice(slab[0][0], slab[1][0] + 1), slice(slab[0][1], slab[1][1] + 1))

        base_height = height_map[slab_pos].max()

        for p in slab_map[slab_pos][(height_map[slab_pos] == base_height) & (slab_map[slab_pos] != 0)]:
            connections_up[p].add(i + 1)
            connections_down[i + 1].add(p)

        # update height map
        height_map[slab_pos] = base_height + slab[1][2] - slab[0][2] + 1

        # update slab map
        slab_map[slab_pos] = i + 1

    return connections_up, connections_down


def part1():
    slabs = parse_input()
    connections_up, connections_down = compute_connections(slabs)

    num_stable_slabs = 0
    for up in connections_up.values():
        if all(len(connections_down[u]) > 1 for u in up):
            num_stable_slabs += 1

    print(num_stable_slabs)


def part2():
    slabs = parse_input()
    connections_up, connections_down = compute_connections(slabs)

    unstable_slabs = set()
    for s, up in connections_up.items():
        if any(len(connections_down[u]) <= 1 for u in up):
            unstable_slabs.add(s)

    def count_collapsed_slabs(s):
        q = [s]
        removed = set()
        while len(q):
            s = q.pop()
            removed.add(s)

            for up in connections_up[s]:
                if len(connections_down[up] - removed) == 0:
                    q.append(up)

        return len(removed) - 1

    c = 0
    for s in unstable_slabs:
        c += count_collapsed_slabs(s)

    print(c)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
