import sys
from functools import cache


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        parts = f.read().strip().split(" ")

    r, c = int(parts[-3][:-1]), int(parts[-1][:-1])

    return r, c


def coord_to_index(r, c):
    diag = r + c - 2
    return (diag * diag + diag) // 2 + c


@cache
def precompute_loop():
    values = [20151125]

    visited = set(values)

    while True:
        next_val = (values[-1] * 252533) % 33554393
        if next_val in visited:
            break
        visited.add(next_val)
        values.append(next_val)

    return values


def code(x):
    loop = precompute_loop()
    return loop[(x - 1) % len(loop)]


def part1():
    r, c = parse_input()

    print(code(coord_to_index(r, c)))


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
