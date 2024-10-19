import sys
from collections import Counter


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return [l.strip() for l in f.readlines() if l.strip()]


def decode_data(data, least_common=False):
    message = []
    for col in zip(*data):
        c = Counter(col).most_common()[-1 if least_common else 0][0]
        message.append(c)
    return "".join(message)


def part1():
    data = parse_input()

    print(decode_data(data, least_common=False))


def part2():
    data = parse_input()

    print(decode_data(data, least_common=True))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
