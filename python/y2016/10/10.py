import sys
from collections import defaultdict


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    inits = []
    bots = {}

    for line in lines:
        parts = line.split(" ")
        if parts[0] == "value":
            inits.append((int(parts[1]), int(parts[-1])))
        else:
            bots[int(parts[1])] = (int(parts[6]), parts[5] == "output", int(parts[-1]), parts[-2] == "output")

    return inits, bots


def simulate_bots(inits, bots):
    bot_chips = defaultdict(list)

    for chip, bot in inits:
        bot_chips[bot].append(chip)

    outputs = {}
    comparisons = {}

    changes = True
    while changes:
        changes = False
        for bot, chips in list(bot_chips.items()):
            if len(chips) == 2:
                changes = True
                chips_sorted = tuple(sorted(chips))
                chips.clear()
                comparisons[chips_sorted] = bot

                low, low_out, high, high_out = bots[bot]
                if low_out:
                    outputs[low] = chips_sorted[0]
                else:
                    bot_chips[low].append(chips_sorted[0])

                if high_out:
                    outputs[high] = chips_sorted[1]
                else:
                    bot_chips[high].append(chips_sorted[1])

    return comparisons, outputs


def part1():
    inits, bots = parse_input()

    comparisons, _ = simulate_bots(inits, bots)
    print(comparisons[(17, 61)])


def part2():
    inits, bots = parse_input()

    _, outputs = simulate_bots(inits, bots)
    print(outputs[0] * outputs[1] * outputs[2])


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
