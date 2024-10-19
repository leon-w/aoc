import sys

import networkx as nx


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    g = nx.Graph()

    for line in lines:
        l, rest = line.split(": ")
        for r in rest.split(" "):
            g.add_edge(l, r)

    return g


def part1():
    g = parse_input()

    g.remove_edges_from(nx.minimum_edge_cut(g))
    comps = [len(c) for c in nx.connected_components(g)]
    print(comps[0] * comps[1])


def part2():
    data = parse_input()


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
