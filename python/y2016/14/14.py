import hashlib
import sys
from functools import cache


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return f.read().strip()


def find_triplet(h):
    for i in range(len(h) - 2):
        if h[i] == h[i + 1] == h[i + 2]:
            return h[i]
    return None


@cache
def hash_(salt, i):
    h = hashlib.md5(f"{salt}{i}".encode("ascii")).hexdigest()
    for _ in range(2016):
        h = hashlib.md5(h.encode("ascii")).hexdigest()
    return h


def check_next_1000(salt, i, t, hash_func):
    for j in range(i + 1, i + 1001):
        if t * 5 in hash_(salt, j):
            return True
    return False


def part1():
    salt = parse_input()
    print(salt)

    i = 0
    hits = []
    # candidates = []
    while len(hits) < 64:
        h = hash_(salt, i)

        t = find_triplet(h)
        if t:
            if check_next_1000(salt, i, t):
                hits.append(i)

        i += 1

    print(hits[-1])


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
