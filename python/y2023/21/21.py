import sys

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    # find S
    x = y = -1
    for y, line in enumerate(lines):
        if "S" in line:
            x = line.index("S")
            break

    c_map = {".": 0, "#": 1, "S": 0}
    grid = np.array([[c_map[c] for c in line] for line in lines], dtype=np.int8)

    return grid, (x, y)


UP = np.array([-1, 0])
DOWN = np.array([1, 0])
LEFT = np.array([0, -1])
RIGHT = np.array([0, 1])


def part1():
    grid, s = parse_input()

    positions = np.zeros_like(grid)
    positions[s] = 1

    for _ in range(64):
        new_postions = np.zeros_like(positions)

        for pos in np.argwhere(positions):
            for d in [UP, DOWN, LEFT, RIGHT]:
                pos_new = pos + d
                if 0 <= pos_new[0] < grid.shape[0] and 0 <= pos_new[1] < grid.shape[1] and grid[*pos_new] == 0:
                    new_postions[*pos_new] = 1

        positions = new_postions

    print(positions.sum())


def part2():
    grid, s = parse_input()

    # compute shortest distance to all tiles
    visited = {}
    q = [(s, 0)]

    while len(q) > 0:
        pos, dist = q.pop(0)

        if pos in visited:
            continue
        visited[pos] = dist

        for d in [UP, DOWN, LEFT, RIGHT]:
            pos_new = (pos[0] + d[0], pos[1] + d[1])

            if 0 <= pos_new[0] < grid.shape[0] and 0 <= pos_new[1] < grid.shape[1] and grid[*pos_new] == 0:
                q.append((pos_new, dist + 1))

    def count_positions(is_even, min_dist=None):
        count = 0
        for d in visited.values():
            if min_dist is not None:
                if d <= min_dist:
                    continue
            if is_even and d % 2 == 1:
                continue
            if not is_even and d % 2 == 0:
                continue
            count += 1
        return count

    # compute total number of tiles after 26501365 steps
    # expression based on: https://www.reddit.com/r/adventofcode/comments/18nol3m/2023_day_21_a_geometric_solutionexplanation_for/
    n = (26501365 - len(grid) // 2) // len(grid)

    total = (
        ((n + 1) ** 2) * count_positions(is_even=False)
        + (n**2) * count_positions(is_even=True)
        - ((n + 1) * count_positions(is_even=False, min_dist=len(grid) // 2))
        + (n * count_positions(is_even=True, min_dist=len(grid) // 2))
    )

    print(total)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
