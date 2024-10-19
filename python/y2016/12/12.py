import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    instructions = []
    for line in lines:
        l, *r = line.split(" ")
        instructions.append((l, r))

    return instructions


def process_instructions(instructions, state):
    def get_operand(op):
        if op in state:
            return state[op]
        else:
            return int(op)

    pc = 0
    while 0 <= pc < len(instructions):
        ins, ops = instructions[pc]
        match ins:
            case "cpy":
                state[ops[1]] = get_operand(ops[0])
            case "inc":
                state[ops[0]] += 1
            case "dec":
                state[ops[0]] -= 1
            case "jnz":
                if get_operand(ops[0]) != 0:
                    pc += get_operand(ops[1]) - 1

        pc += 1

    return state


def part1():
    instructions = parse_input()
    state = {
        "a": 0,
        "b": 0,
        "c": 0,
        "d": 0,
    }

    state = process_instructions(instructions, state)
    print(state["a"])


def part2():
    instructions = parse_input()
    state = {
        "a": 0,
        "b": 0,
        "c": 1,
        "d": 0,
    }

    state = process_instructions(instructions, state)
    print(state["a"])


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
