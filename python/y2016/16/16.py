import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return f.read().strip()


def generate_data(a, l):
    while len(a) < l:
        b = "".join("1" if c == "0" else "0" for c in a[::-1])
        a = f"{a}0{b}"

    return a


def checksum(s):
    while len(s) % 2 == 0:
        s = "".join("1" if s[i] == s[i + 1] else "0" for i in range(0, len(s), 2))

    return s


def part1():
    data = parse_input()

    l = 272

    print(checksum(generate_data(data, l)[:l]))


def part2():
    data = parse_input()

    l = 35651584

    print(checksum(generate_data(data, l)[:l]))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
