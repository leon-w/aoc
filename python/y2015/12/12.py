import json
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return json.load(f)


def part1():
    data = parse_input()

    def object_sum(obj):
        if isinstance(obj, int):
            return obj

        if isinstance(obj, list):
            return sum(object_sum(el) for el in obj)

        if isinstance(obj, dict):
            return sum(object_sum(el) for el in obj.values())

        return 0

    print(object_sum(data))


def part2():
    data = parse_input()

    def object_sum_no_red(obj):
        if isinstance(obj, int):
            return obj

        if isinstance(obj, list):
            return sum(object_sum_no_red(el) for el in obj)

        if isinstance(obj, dict):
            if "red" in obj.values():
                return 0
            return sum(object_sum_no_red(el) for el in obj.values())

        return 0

    print(object_sum_no_red(data))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
