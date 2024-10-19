import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return [tuple(int(n) for n in l.strip().split("-")) for l in f.readlines() if l.strip()]


def part1():
    ranges = parse_input()
    ranges.sort()

    i = 0
    for start, end in ranges:
        if i < start:
            print(i + 1)
            break
        i = max(i, end)


def part2():
    ranges = parse_input()
    ranges.sort()

    total = 0
    i = 0
    for start, end in ranges:
        if i < start:
            total += start - i - 1
        i = max(i, end)

    print(total)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
