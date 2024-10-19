import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return f.read().strip()


def part1():
    data = parse_input()

    l = 0
    i = 0
    while i < len(data):
        if data[i] == "(":
            marker_len = data[i:].index(")")
            span, repeat = map(int, data[i + 1 : i + marker_len].split("x"))
            l += span * repeat
            i += marker_len + span + 1
        else:
            l += 1
            i += 1

    print(l)


def part2():
    data = parse_input()

    def get_decompressed_len(data):
        l = 0
        i = 0
        while i < len(data):
            if data[i] == "(":
                marker_len = data[i:].index(")")
                span, repeat = map(int, data[i + 1 : i + marker_len].split("x"))
                i += marker_len + 1

                rep = data[i : i + span]
                l += get_decompressed_len(rep) * repeat
                i += span
            else:
                l += 1
                i += 1

        return l

    print(get_decompressed_len(data))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
