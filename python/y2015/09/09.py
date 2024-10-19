import itertools
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    distances = {}
    locations = set()
    for line in lines:
        start, _, end, _, d = line.split(" ")
        d = int(d)
        distances[(start, end)] = d
        distances[(end, start)] = d
        locations.add(start)
        locations.add(end)

    return distances, locations


def route_distances(distances, locations):
    # brute force Traveling Salesperson problem
    for order in itertools.permutations(locations):
        dist = 0
        for i in range(len(order) - 1):
            dist += distances[(order[i], order[i + 1])]
        yield dist


def part1():
    distances, locations = parse_input()

    print(min(route_distances(distances, locations)))


def part2():
    distances, locations = parse_input()

    print(max(route_distances(distances, locations)))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
