import itertools
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return [int(l.strip()) for l in f.readlines() if l.strip()]


def part1():
    containers = parse_input()

    count = 0
    for selection in itertools.product([False, True], repeat=len(containers)):
        if sum(itertools.compress(containers, selection)) == 150:
            count += 1

    print(count)


def part2():
    containers = parse_input()

    amounts = []
    for selection in itertools.product([False, True], repeat=len(containers)):
        if sum(itertools.compress(containers, selection)) == 150:
            amounts.append(sum(selection))

    print(amounts.count(min(amounts)))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
