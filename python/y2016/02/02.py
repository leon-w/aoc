import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return [l.strip() for l in f.readlines() if l.strip()]


def part1():
    seqs = parse_input()

    x = 1
    y = 1
    digits = []

    for seq in seqs:
        for c in seq:
            match c:
                case "U":
                    if y > 0:
                        y -= 1
                case "R":
                    if x < 2:
                        x += 1
                case "D":
                    if y < 2:
                        y += 1
                case "L":
                    if x > 0:
                        x -= 1

        digits.append(str(y * 3 + x + 1))

    print("".join(digits))


def part2():
    seqs = parse_input()

    x = -2
    y = 0
    digits = []

    for seq in seqs:
        for c in seq:
            match c:
                case "U":
                    if abs(x) - y != 2:
                        y -= 1
                case "R":
                    if abs(y) + x != 2:
                        x += 1
                case "D":
                    if abs(x) + y != 2:
                        y += 1
                case "L":
                    if abs(y) - x != 2:
                        x -= 1

        digit = [0, 1, 4, 9, 12][y + 2] + [0, 1, 2, 1, 0][y + 2] + x
        digits.append("123456789ABCD"[digit])

    print("".join(digits))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
