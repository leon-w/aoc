import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return f.read().strip()


rules = set(["^^.", ".^^", "^..", "..^"])


def count_safe_tiles(state, generations):
    safe = 0
    for _ in range(generations):
        safe += state.count(".")
        state = f".{state}."
        state = "".join("^" if state[i : i + 3] in rules else "." for i in range(len(state) - 2))
    return safe


def part1():
    state = parse_input()

    print(count_safe_tiles(state, 40))


def part2():
    state = parse_input()

    print(count_safe_tiles(state, 400000))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
