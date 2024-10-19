import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l]

    cards = []

    def to_numbers(s):
        return [int(s[i : i + 2].strip()) for i in range(0, len(s), 3)]

    for line in lines:
        l, r = line.split(": ")[-1].split(" | ")
        l = to_numbers(l)
        r = to_numbers(r)

        cards.append((l, r))

    return cards


def part1():
    data = parse_input()

    points_sum = 0
    for l, r in data:
        matches = len(set(l).intersection(r))
        if matches:
            points_sum += 2 ** (matches - 1)

    print(f"Point sum: {points_sum}")


def part2():
    data = parse_input()
    card_wins = [len(set(l).intersection(r)) for (l, r) in data]

    ns = [1] * len(card_wins)

    for i in range(len(ns)):
        for j in range(card_wins[i]):
            ns[i + j + 1] += ns[i]

    print(f"Total cards: {sum(ns)}")


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
