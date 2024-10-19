import multiprocessing
import random
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    hp, dmg = [int(l.split(": ")[-1]) for l in lines]
    return hp, dmg


spells = [
    ("magic_missile", 53),
    ("drain", 73),
    ("shield", 113),
    ("poison", 173),
    ("recharge", 229),
]


def simulate_random_game(boss):
    while True:
        boss_hp, boss_dmg, hard = boss
        hp = 50
        armor = 0
        mana = 500

        effect_shield = 0
        effect_poison = 0
        effect_recharge = 0

        my_turn = True

        mana_spent = 0
        while True:
            # process effects
            if effect_shield > 0:
                armor = 7
                effect_shield -= 1
                if effect_shield == 0:
                    armor = 0

            if effect_poison > 0:
                boss_hp -= 3
                if boss_hp <= 0:
                    return mana_spent
                effect_poison -= 1

            if effect_recharge > 0:
                mana += 101
                effect_recharge -= 1

            # take turns
            if my_turn:
                if hard:
                    hp -= 1
                    if hp <= 0:
                        break

                possible_spells = [spell for spell in spells if spell[1] <= mana]

                if len(possible_spells) == 0:
                    break

                spell = random.choice(possible_spells)

                mana -= spell[1]
                mana_spent += spell[1]

                match spell[0]:
                    case "magic_missile":
                        boss_hp -= 4
                    case "drain":
                        hp += 2
                        boss_hp -= 2
                    case "shield":
                        effect_shield = 6
                    case "poison":
                        effect_poison = 6
                    case "recharge":
                        effect_recharge = 5

            else:
                hp -= max(1, boss_dmg - armor)

            if hp <= 0:
                break

            if boss_hp <= 0:
                return mana_spent

            my_turn = not my_turn


def part1():
    boss_hp, boss_dmg = parse_input()
    hard = False

    random.seed(42)

    total_candidates = 10
    with multiprocessing.Pool() as p:
        candidates = p.map(simulate_random_game, [(boss_hp, boss_dmg, hard)] * total_candidates)

    print(min(candidates))


def part2():
    boss_hp, boss_dmg = parse_input()
    hard = True

    random.seed(42)

    total_candidates = 10
    with multiprocessing.Pool() as p:
        candidates = p.map(simulate_random_game, [(boss_hp, boss_dmg, hard)] * total_candidates)

    print(min(candidates))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
