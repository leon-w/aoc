import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return f.read().strip()


def process_sequence(sequence, iterations):
    sequence = [int(d) for d in sequence]
    for _ in range(iterations):
        new_sequence = []
        i = 0

        while i < len(sequence):
            d = sequence[i]
            l = 1
            for j in range(i + 1, len(sequence)):
                if sequence[j] == d:
                    l += 1
                else:
                    break
            new_sequence.append(l)
            new_sequence.append(d)
            i += l

        sequence = new_sequence

    return len(sequence)


def part1():
    sequence = parse_input()

    print(process_sequence(sequence, 40))


def part2():
    sequence = parse_input()

    print(process_sequence(sequence, 50))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
