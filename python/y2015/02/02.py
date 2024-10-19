import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    return [[int(n) for n in line.split("x")] for line in lines]


def part1():
    boxes = parse_input()

    total = 0
    for a, b, c in boxes:
        areas = [a * b, b * c, c * a]
        total += sum(areas) * 2 + min(areas)

    print(total)


def part2():
    boxes = parse_input()

    total = 0
    for a, b, c in boxes:
        total += min(a + b, b + c, c + a) * 2 + a * b * c

    print(total)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
