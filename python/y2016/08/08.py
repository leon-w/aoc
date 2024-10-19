import sys

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    instructions = []
    for line in lines:
        parts = line.split(" ")
        if parts[0] == "rect":
            parts_r = parts[1].split("x")
            instructions.append(("rect", int(parts_r[0]), int(parts_r[1])))
        elif parts[0] == "rotate":
            instructions.append((parts[1], int(parts[2].split("=")[-1]), int(parts[-1])))

    return instructions


def apply_instructions_to_screen(instructions):
    screen = np.zeros((6, 50), dtype=np.bool_)

    for t, a, b in instructions:
        match t:
            case "rect":
                screen[:b, :a] = True
            case "row":
                screen[a] = np.roll(screen[a], b)
            case "column":
                screen[:, a] = np.roll(screen[:, a], b)

    return screen


def part1():
    instructions = parse_input()

    screen = apply_instructions_to_screen(instructions)

    print(np.count_nonzero(screen))


def part2():
    instructions = parse_input()

    screen = apply_instructions_to_screen(instructions)

    # we could implement automatic letter matching in the output but will omit it here for now

    for row in screen:
        for pixel in row:
            print(end="#" if pixel else ".")
        print()


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
