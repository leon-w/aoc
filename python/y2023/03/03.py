import sys
from collections import defaultdict


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l]

    return lines


def part1():
    data = parse_input()
    data = [l + "." for l in data]  # pad right

    symbols = set("#@%-+&$=*/")
    numbers = set("0123456789")

    part_sum = 0
    for y, l in enumerate(data):
        n_idx = None
        for x, c in enumerate(l):
            if c in numbers:
                if n_idx is None:
                    n_idx = x
            else:
                if n_idx is not None:
                    n = int(l[n_idx:x])

                    x0 = max(0, n_idx - 1)
                    x1 = min(len(l) - 1, x)
                    y0 = max(0, y - 1)
                    y1 = min(len(data) - 1, y + 1)

                    surr = set()
                    for ys in range(y0, y1 + 1):
                        surr.update(data[ys][x0 : x1 + 1])

                    if not symbols.isdisjoint(surr):
                        part_sum += n

                    n_idx = None

    print(f"Part sum: {part_sum}")


def part2():
    data = parse_input()
    data = [l + "." for l in data]  # pad right

    numbers = set("0123456789")

    gears = defaultdict(list)

    for y, l in enumerate(data):
        n_idx = None
        for x, c in enumerate(l):
            if c in numbers:
                if n_idx is None:
                    n_idx = x
            else:
                if n_idx is not None:
                    n = int(l[n_idx:x])

                    x0 = max(0, n_idx - 1)
                    x1 = min(len(l) - 1, x)
                    y0 = max(0, y - 1)
                    y1 = min(len(data) - 1, y + 1)

                    for ys in range(y0, y1 + 1):
                        for xs in range(x0, x1 + 1):
                            if data[ys][xs] == "*":
                                gears[(ys, xs)].append(n)

                    n_idx = None

    gear_sum = 0
    for ns in gears.values():
        if len(ns) == 2:
            gear_sum += ns[0] * ns[1]

    print(f"Gear sum: {gear_sum}")


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
