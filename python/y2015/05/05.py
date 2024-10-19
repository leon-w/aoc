import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    return lines


def part1():
    data = parse_input()

    count = 0
    for s in data:
        vowels = 0
        for c in s:
            vowels += c in "aeiou"
        if vowels < 3:
            continue

        double_letter = False
        for i in range(len(s) - 1):
            if s[i] == s[i + 1]:
                double_letter = True
                break
        if not double_letter:
            continue

        if not all(x not in s for x in ["ab", "cd", "pq", "xy"]):
            continue

        count += 1

    print(count)


def part2():
    data = parse_input()

    count = 0
    for s in data:
        double_pair = False
        for i in range(max(0, len(s) - 3)):
            double = s[i : i + 2]
            if double in s[i + 2 :]:
                double_pair = True
                break
        if not double_pair:
            continue

        repeat = False
        for i in range(max(0, len(s) - 2)):
            if s[i] == s[i + 2]:
                repeat = True
        if not repeat:
            continue

        count += 1

    print(count)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
