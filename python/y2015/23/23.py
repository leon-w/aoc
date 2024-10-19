import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    instructions = []
    for line in lines:
        ins, ops = line.split(" ", maxsplit=1)
        instructions.append((ins, ops.split(", ")))

    return instructions


def simulate_machine(instructions, registers):
    pc = 0
    while 0 <= pc < len(instructions):
        ins, ops = instructions[pc]

        match ins:
            case "hlf":
                registers[ops[0]] //= 2
            case "tpl":
                registers[ops[0]] *= 3
            case "inc":
                registers[ops[0]] += 1
            case "jmp":
                pc += int(ops[0]) - 1
            case "jie":
                if registers[ops[0]] % 2 == 0:
                    pc += int(ops[1]) - 1
            case "jio":
                if registers[ops[0]] == 1:
                    pc += int(ops[1]) - 1

        pc += 1

    return registers


def part1():
    instructions = parse_input()

    registers = simulate_machine(instructions, {"a": 0, "b": 0})
    print(registers["b"])


def part2():
    instructions = parse_input()

    registers = simulate_machine(instructions, {"a": 1, "b": 0})
    print(registers["b"])


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
