import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    aunts = []
    for line in lines:
        props = line.split(": ", maxsplit=1)[1].split(", ")
        aunt = {}
        for prop in props:
            k, v = prop.split(": ")
            aunt[k] = int(v)

        aunts.append(aunt)

    return aunts


requirements = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def find_aunt_1(aunts):
    for i, aunt in enumerate(aunts):
        possible = True
        for k, v in aunt.items():
            if requirements[k] != v:
                possible = False
                break

        if possible:
            return i + 1

    raise ValueError


def find_aunt_2(aunts):
    last_sol = find_aunt_1(aunts)

    for i, aunt in enumerate(aunts):
        possible = True
        for k, v in aunt.items():
            if k in ["cats", "trees"]:
                if requirements[k] > v:
                    possible = False
                    break
            elif k in ["pomeranians", "goldfish"]:
                if requirements[k] < v:
                    possible = False
                    break
            else:
                if requirements[k] != v:
                    possible = False
                    break

        if possible and i != last_sol - 1:
            return i + 1

    raise ValueError


def part1():
    aunts = parse_input()

    print(find_aunt_1(aunts))


def part2():
    aunts = parse_input()

    print(find_aunt_2(aunts))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
