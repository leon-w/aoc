import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    instructions = []
    for line in lines:
        if "#" in line:
            line = line[: line.index("#") - 1].strip()
        l, *r = line.split(" ")
        instructions.append([l, r])

    return instructions


def process_instructions(instructions, state):
    def get_operand(op):
        if op in state:
            return state[op]
        else:
            return int(op)

    for x in instructions:
        x.append(0)

    pc = 0
    while 0 <= pc < len(instructions):
        instructions[pc][2] += 1
        ins, ops, _ = instructions[pc]
        match ins:
            case "cpy":
                if ops[1] in state:
                    state[ops[1]] = get_operand(ops[0])
            case "inc":
                if ops[0] in state:
                    state[ops[0]] += 1
            case "dec":
                if ops[0] in state:
                    state[ops[0]] -= 1
            case "jnz":
                if get_operand(ops[0]) != 0:
                    pc += get_operand(ops[1]) - 1
            case "tgl":
                target_index = pc + get_operand(ops[0])
                if 0 <= target_index < len(instructions):
                    target = instructions[target_index]
                    target_ins, target_ops, _ = target
                    if len(target_ops) == 1:
                        if target_ins == "inc":
                            target[0] = "dec"
                        else:
                            target[0] = "inc"
                    elif len(target_ops) == 2:
                        if target_ins == "jnz":
                            target[0] = "cpy"
                        else:
                            target[0] = "jnz"
            case "mul":
                if ops[2] in state:
                    state[ops[2]] = get_operand(ops[0]) * get_operand(ops[1])
            case "add":
                if ops[1] in state:
                    state[ops[1]] += get_operand(ops[0])
            case "nop":
                pass
            case _:
                print(f"invalid instruction:", ins, *ops)

        pc += 1

    return state


def part1():
    instructions = parse_input()
    state = {
        "a": 7,
        "b": 0,
        "c": 0,
        "d": 0,
    }

    state = process_instructions(instructions, state)
    print(state["a"])


def part2():
    instructions = parse_input()
    state = {
        "a": 12,
        "b": 0,
        "c": 0,
        "d": 0,
    }

    # the solution to this puzzle is to replace the loop with a multiplication
    # To preserve addresses, we use [cpy a a] as a nop
    # cpy 0 c    <--  cpy b c
    # mul d b a  <--  inc a
    # cpy a a    <--  dec c
    # cpy a a    <--  jnz c -2
    # cpy a a    <--  dec d
    # cpy a a    <--  jnz d -5

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
