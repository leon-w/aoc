import hashlib
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return f.read().strip()


def find_seed(secret, n_zeros):
    i = 0
    zeros = "0" * n_zeros
    while True:
        s = f"{secret}{i}"
        h = hashlib.md5(s.encode()).digest().hex()
        if h.startswith(zeros):
            return i
        i += 1


def part1():
    secret = parse_input()
    print(find_seed(secret, 5))


def part2():
    secret = parse_input()
    print(find_seed(secret, 6))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
