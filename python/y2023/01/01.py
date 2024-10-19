import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return [l.strip() for l in f.readlines() if l]


def part1():
    input_lines = parse_input()

    total_sum = 0
    for l in input_lines:
        digits = [int(c) for c in l.strip() if c in "0123456789"]
        total_sum += digits[0] * 10 + digits[-1]

    print(f"Total: {total_sum}")


def part2():
    input_lines = parse_input()

    letter_mapping = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    total_sum = 0

    for l in input_lines:
        digits = []

        i = 0
        while i < len(l):
            for k, v in letter_mapping.items():
                if l[i:].startswith(k):
                    digits.append(v)
                    break
            if l[i] in "0123456789":
                digits.append(int(l[i]))
            i += 1

        total_sum += digits[0] * 10 + digits[-1]

    print(f"Total: {total_sum}")


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")

    print(">>> Part 2 <<<")
    part2()
    print("==============")
