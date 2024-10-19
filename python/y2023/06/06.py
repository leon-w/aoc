import math
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    def parse_numbers(l: str):
        l = l.split(":")[-1]
        return [int(s) for s in l.split()]

    return parse_numbers(lines[0]), parse_numbers(lines[1])


def compute_options(t, d):
    # brute force, still feasible
    # n = 0
    # for i in range(1, t):
    #     dt = i * (t - i)
    #     n += dt > d

    # direct computation is a lot faster
    t2 = t / 2
    r = math.sqrt(t2 * t2 - d)
    s1 = math.ceil(t2 - r)
    s2 = math.floor(t2 + r)
    n = s2 - s1 + 1

    return n


def part1():
    ts, ds = parse_input()

    prod = 1

    for t, d in zip(ts, ds):
        n = compute_options(t, d)
        prod *= n

    print(f"Product: {prod}")


def part2():
    ts, ds = parse_input()

    t = int("".join(map(str, ts)))
    d = int("".join(map(str, ds)))

    n = compute_options(t, d)

    print(f"Total: {n}")


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
