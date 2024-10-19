import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return f.read().strip()


def part1():
    seq = parse_input()

    visited = set()
    x = y = 0
    visited.add((0, 0))
    for c in seq:
        match c:
            case "^":
                y -= 1
            case ">":
                x += 1
            case "v":
                y += 1
            case "<":
                x -= 1
        visited.add((x, y))

    print(len(visited))


def part2():
    seq = parse_input()

    visited = set()
    p1, p2 = [0, 0], [0, 0]
    visited.add((0, 0))
    for i, c in enumerate(seq):
        p = p1 if i % 2 else p2
        match c:
            case "^":
                p[1] -= 1
            case ">":
                p[0] += 1
            case "v":
                p[1] += 1
            case "<":
                p[0] -= 1
        visited.add((p[0], p[1]))

    print(len(visited))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
