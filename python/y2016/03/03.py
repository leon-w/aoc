import itertools
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return [[int(d) for d in l.strip().split()] for l in f.readlines() if l.strip()]


def count_valid_triangles(triangles):
    count = 0
    for a, b, c in triangles:
        if a > b and a > c:
            count += a < b + c
        elif b > a and b > c:
            count += b < a + c
        else:
            count += c < a + b
    return count


def part1():
    triangles = parse_input()

    print(count_valid_triangles(triangles))


def part2():
    data = parse_input()

    # requires at least python 3.12 for `itertools.batched`
    triangles = itertools.batched(itertools.chain(*zip(*data)), 3)
    print(count_valid_triangles(triangles))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
