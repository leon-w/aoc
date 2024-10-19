import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    return lines


def part1():
    data = parse_input()

    total = 0
    for line in data:
        len_bytes = 0

        i = 1
        while i < len(line) - 1:
            len_bytes += 1
            if line[i] == "\\":
                if line[i + 1] == "x":
                    i += 3
                else:
                    i += 1
            i += 1

        total += len(line) - len_bytes

    print(total)


def part2():
    data = parse_input()

    total = 0
    for line in data:
        total += line.count('"') + line.count("\\") + 2

    print(total)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
