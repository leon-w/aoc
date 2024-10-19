import itertools
import re
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    nodes = []
    for line in lines:
        if m := re.match(r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T", line):
            nodes.append(tuple(map(int, m.groups())))

    return nodes


def part1():
    nodes = parse_input()

    count = 0
    for a, b in itertools.product(nodes, repeat=2):
        if a != b and a[3] != 0 and a[3] <= b[2] - b[3]:
            count += 1

    print(count)


def part2():
    data = parse_input()

    max_x = max(x for x, _, _, _ in data)
    max_y = max(y for _, y, _, _ in data)

    grid = [[(0, 0) for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for x, y, size, used in data:
        grid[y][x] = (size, used)

    empty = (0, 0)
    empty_capacity = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell[1] == 0:
                empty = (x, y)
                empty_capacity = cell[0]
                break
        if empty:
            break

    # print grid
    # for row in grid:
    #     for cell in row:
    #         if cell[1] == 0:
    #             print("_", end=" ")
    #         elif cell[1] > empty_capacity:
    #             print("#", end=" ")
    #         else:
    #             print(".", end=" ")
    #     print()

    moves = empty[0] + empty[1] + max_x
    moves += (max_x - 1) * 5

    print(moves)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
