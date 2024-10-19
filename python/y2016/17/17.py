import hashlib
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return f.read().strip()


def find_path(salt, find_longest=False):
    q = []
    q.append(((0, 0), ""))

    longest_path = ""

    while len(q):
        (x, y), path = q.pop(0)

        if x == 3 and y == 3:
            if find_longest:
                longest_path = path if len(path) > len(longest_path) else longest_path
                continue
            else:
                return path

        h = hashlib.md5((salt + path).encode()).digest().hex()
        u, d, l, r = (int(c, 16) >= 11 for c in h[:4])

        if u and 0 <= y - 1:
            q.append(((x, y - 1), path + "U"))
        if d and y + 1 <= 3:
            q.append(((x, y + 1), path + "D"))
        if l and 0 <= x - 1:
            q.append(((x - 1, y), path + "L"))
        if r and x + 1 <= 3:
            q.append(((x + 1, y), path + "R"))

    return longest_path


def part1():
    salt = parse_input()
    print(find_path(salt))


def part2():
    salt = parse_input()
    print(len(find_path(salt, find_longest=True)))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
