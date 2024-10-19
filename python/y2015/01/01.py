import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return f.read().strip()


def part1():
    data = parse_input()

    ob = data.count("(")
    cb = data.count(")")

    print(ob - cb)


def part2():
    data = parse_input()

    pos = 0
    for i, c in enumerate(data):
        if c == "(":
            pos += 1
        else:
            pos -= 1

        if pos == -1:
            print(i + 1)
            break


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
