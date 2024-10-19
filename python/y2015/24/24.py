import itertools
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]


def find_min_weight_count(weights, target_weight):
    weights = sorted(weights, reverse=True)
    w = 0
    for i in range(len(weights)):
        w += weights[i]
        if w >= target_weight:
            return i + 1

    raise ValueError


def can_be_split(weights, groups):
    target_weight = sum(weights) // groups
    size = find_min_weight_count(weights, target_weight)
    # there must be at least one group which is not larger than 1/3 of the total weights
    while size <= len(weights) / groups:
        for wi in itertools.combinations(range(len(weights)), size):
            if sum(weights[i] for i in wi) == target_weight:
                if groups > 2:
                    remaining_weights = [weights[i] for i in range(len(weights)) if i not in wi]
                    if can_be_split(remaining_weights, groups - 1):
                        return True
                else:
                    return True
        size += 1

    return False


def compute_min_qe(weights, groups):
    def qe(weights):
        prod = 1
        for w in weights:
            prod *= w
        return prod

    target_weight = sum(weights) // groups

    size = find_min_weight_count(weights, target_weight)
    while True:
        solution = False
        min_qe = float("inf")

        for wi in itertools.combinations(range(len(weights)), size):
            selected_weights = [weights[i] for i in wi]
            if sum(selected_weights) == target_weight:
                remaining_weights = [weights[i] for i in range(len(weights)) if i not in wi]
                if can_be_split(remaining_weights, groups):
                    solution = True
                    min_qe = min(min_qe, qe(selected_weights))

        if solution:
            return min_qe

        size += 1


def part1():
    weights = parse_input()

    print(compute_min_qe(weights, groups=3))


def part2():
    weights = parse_input()

    print(compute_min_qe(weights, groups=4))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
