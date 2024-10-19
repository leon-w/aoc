import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    ingredients = []

    for line in lines:
        ingredient = {}
        _, stats = line.split(": ")
        for stat in stats.split(", "):
            name, val = stat.split(" ")
            ingredient[name] = int(val)
        ingredients.append(ingredient)

    return ingredients


# this only works if we have exactly 4 ingredients
def compute_scores(ingredients, required_calories=None):
    props = ["capacity", "durability", "flavor", "texture", "calories"]
    for a1 in range(101):
        for a2 in range(101 - a1):
            for a3 in range(101 - a1 - a2):
                sizes = [a1, a2, a3, 100 - a1 - a2 - a3]
                scores = [0, 0, 0, 0, 0]
                for size, ingredient in zip(sizes, ingredients):
                    for i, prop in enumerate(props):
                        scores[i] += ingredient[prop] * size

                if required_calories is not None:
                    if scores[-1] != required_calories:
                        continue

                prod = 1
                for score in scores[:-1]:
                    prod *= max(0, score)

                yield prod


def part1():
    ingredients = parse_input()

    print(max(compute_scores(ingredients)))


def part2():
    ingredients = parse_input()

    print(max(compute_scores(ingredients, required_calories=500)))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
