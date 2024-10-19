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


def part1():
    instructions = parse_input()

    a = 0
    while True:
        state = {
            "a": a,
            "b": 0,
            "c": 0,
            "d": 0,
        }

        output = []

        def get_operand(op):
            return state[op] if op in state else int(op)

        pc = 0

        known_states = {}

        while 0 <= pc < len(instructions):
            ins, ops = instructions[pc]
            match ins:
                case "cpy":
                    state[ops[1]] = get_operand(ops[0])
                case "inc":
                    state[ops[0]] += 1
                case "dec":
                    state[ops[0]] -= 1
                case "out":
                    output.append(get_operand(ops[0]))
                    if len(output) == 1:
                        if output[0] != 0:
                            break
                    if len(output) > 1:
                        o2 = output[-2]
                        o1 = output[-1]
                        if not ((o1 == 1 and o2 == 0) or (o1 == 0 and o2 == 1)):
                            break
                case "jnz":
                    if get_operand(ops[0]) != 0:
                        pc += get_operand(ops[1]) - 1

            pc += 1

            frozen_state = (*sorted(state.items()), pc)

            if frozen_state in known_states:
                l = known_states[frozen_state]
                if len(output) >= l + 2:
                    print(a)
                    return
                break

            known_states[frozen_state] = len(output)

        a += 1


def part2():
    instructions = parse_input()


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
