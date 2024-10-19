import sys

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    def parse_operand(op):
        if op.isdigit():
            return np.uint16(int(op))
        return op

    instructions = []
    for line in lines:
        l, r = line.split(" -> ")
        l_parts = l.split(" ")

        if len(l_parts) == 1:
            t = "ID"
            ops = [parse_operand(l_parts[0])]
        elif len(l_parts) == 2:
            t = "NOT"
            ops = [parse_operand(l_parts[1])]
        else:
            t = l_parts[1]
            ops = [parse_operand(l_parts[0]), parse_operand(l_parts[2])]
        instructions.append((t, ops, r))

    return instructions


def process_instructions(instructions, known_values):
    new_values = True
    while new_values > 0:
        new_values = False
        for t, ops, r in instructions:
            if r in known_values:
                continue

            ops_fetched = []
            for op in ops:
                if isinstance(op, str):
                    if op in known_values:
                        ops_fetched.append(known_values[op])
                    else:
                        break
                else:
                    ops_fetched.append(op)

            if len(ops_fetched) != len(ops):
                continue

            match t:
                case "ID":
                    rval = ops_fetched[0]
                case "NOT":
                    rval = ~ops_fetched[0]
                case "AND":
                    rval = ops_fetched[0] & ops_fetched[1]
                case "OR":
                    rval = ops_fetched[0] | ops_fetched[1]
                case "LSHIFT":
                    rval = ops_fetched[0] << ops_fetched[1]
                case "RSHIFT":
                    rval = ops_fetched[0] >> ops_fetched[1]
                case _:
                    raise

            known_values[r] = rval
            new_values = True

    return known_values


def part1():
    instructions = parse_input()

    results = process_instructions(instructions, {})
    print(results["a"])


def part2():
    instructions = parse_input()

    x = process_instructions(instructions, {})["a"]
    results = process_instructions(instructions, {"b": x})
    print(results["a"])


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
