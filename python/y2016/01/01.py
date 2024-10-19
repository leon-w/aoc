import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return [(s[0], int(s[1:])) for s in f.read().strip().split(", ")]


def find_distance(steps, return_first_double_visited):
    x = 0
    y = 0
    d = 0

    visited = set()
    visited.add((x, y))

    for turn, l in steps:
        d = (d + (-1 if turn == "L" else 1)) % 4
        for _ in range(l):
            match d:
                case 0:
                    y += 1
                case 1:
                    x += 1
                case 2:
                    y -= 1
                case 3:
                    x -= 1

            if return_first_double_visited:
                if (x, y) in visited:
                    return abs(x) + abs(y)

                visited.add((x, y))

    return abs(x) + abs(y)


def part1():
    steps = parse_input()
    print(find_distance(steps, return_first_double_visited=False))


def part2():
    steps = parse_input()
    print(find_distance(steps, return_first_double_visited=True))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
