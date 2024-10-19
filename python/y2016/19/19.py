import math
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return int(f.read().strip())


def compute_winning_1(n):
    # eliminate next
    # winner = 1
    # i = 1
    # while n > 1:
    #     n, r = divmod(n, 2)
    #     if r:
    #         winner += 2**i
    #     i += 1
    # return winner

    return (n - 2 ** int(math.log2(n))) * 2 + 1


def compute_winning_2(n):
    # i = 1

    # while i * 3 < n:
    #     i *= 3

    # return n - i

    return n - 3 ** int(math.log(n - 1, 3))


def part1():
    n = parse_input()

    print(compute_winning_1(n))


def part2():
    n = parse_input()

    print(compute_winning_2(n))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
