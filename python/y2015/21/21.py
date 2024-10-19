import itertools
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    hp, dmg, armor = [int(l.split(": ")[-1]) for l in lines]
    return hp, dmg, armor


def determine_win(p1, p2):
    hp_p1, dmg_p1, arm_p1 = p1
    hp_p2, dmg_p2, arm_p2 = p2
    while True:
        dmg = max(1, dmg_p1 - arm_p2)
        hp_p2 -= dmg
        if hp_p2 <= 0:
            return True

        dmg = max(1, dmg_p2 - arm_p1)
        hp_p1 -= dmg
        if hp_p1 <= 0:
            return False


weapons = [(8, 4, 0), (10, 5, 0), (25, 6, 0), (40, 7, 0), (74, 8, 0)]
armor = [(0, 0, 0), (13, 0, 1), (31, 0, 2), (53, 0, 3), (75, 0, 4), (102, 0, 5)]
rings = [(0, 0, 0), (0, 0, 0), (25, 1, 0), (50, 2, 0), (100, 3, 0), (20, 0, 1), (40, 0, 2), (80, 0, 3)]


def compute_costs(enemy, win=True):
    for w in weapons:
        for a in armor:
            for rs in itertools.combinations(rings, 2):
                hp, dmg, arm = 100, 0, 0
                cost = 0
                for item_price, item_dmg, item_arm in [w, a, *rs]:
                    cost += item_price
                    dmg += item_dmg
                    arm += item_arm

                if determine_win((hp, dmg, arm), enemy) == win:
                    yield cost


def part1():
    enemy = parse_input()

    print(min(compute_costs(enemy)))


def part2():
    enemy = parse_input()

    print(max(compute_costs(enemy, win=False)))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
