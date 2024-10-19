import sys

import sympy


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return int(f.read().strip())


def part1():
    limit = parse_input()

    i = 1
    while 10 * sum(sympy.divisors(i, generator=True)) < limit:
        i += 1

    print(i)


def part2():
    limit = parse_input()

    def get_points(n):
        points = 0
        for d in sympy.divisors(n, generator=True):
            if n // d <= 50:
                points += d

        return points * 11

    i = 1
    while get_points(i) < limit:
        i += 1

    print(i)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
