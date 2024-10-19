import hashlib
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return f.read().strip()


def part1():
    door_id = parse_input()

    password = []
    i = 0
    while len(password) < 8:
        h = hashlib.md5(f"{door_id}{i}".encode("ascii")).digest().hex()
        if h.startswith("00000"):
            password.append(h[5])
        i += 1
    print("".join(password))


def part2():
    door_id = parse_input()

    password = [None] * 8
    i = 0
    while password.count(None) > 0:
        h = hashlib.md5(f"{door_id}{i}".encode("ascii")).digest().hex()
        if h.startswith("00000") and h[5] in "01234567":
            idx = int(h[5])
            if password[idx] is None:
                password[idx] = h[6]
        i += 1
    print("".join(password))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
