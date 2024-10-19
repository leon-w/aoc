import sys
from dataclasses import dataclass, field
from queue import PriorityQueue

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [list(l.strip()) for l in f.readlines() if l.strip()]

    grid = np.array(lines, dtype=np.int64)

    return grid


class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vec({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))


UP = Vec(0, -1)
LEFT = Vec(-1, 0)
DOWN = Vec(0, 1)
RIGHT = Vec(1, 0)


def find_shortest_path(grid, min_steps, max_steps, target):
    @dataclass(order=True)
    class QueueItem:
        distance: int
        p: Vec = field(compare=False)
        horizontal: bool = field(compare=False)

    visited = np.full((2, *grid.shape), 0)

    q = PriorityQueue()

    q.put(QueueItem(0, Vec(0, 0), True))
    q.put(QueueItem(0, Vec(0, 0), False))

    while not q.empty():
        item = q.get()

        if item.p == target:
            return item.distance

        if visited[int(item.horizontal), item.p.y, item.p.x]:
            continue

        visited[int(item.horizontal), item.p.y, item.p.x] = 1

        for direction in [LEFT, RIGHT] if item.horizontal else [UP, DOWN]:
            d_new = item.distance
            p_new = item.p
            for i in range(max_steps):
                p_new = p_new + direction
                if 0 <= p_new.x < grid.shape[1] and 0 <= p_new.y < grid.shape[0]:
                    d_new += grid[p_new.y, p_new.x]

                    if i < min_steps - 1:
                        continue

                    if not visited[int(item.horizontal), p_new.y, p_new.x]:
                        q.put(QueueItem(d_new, p_new, not item.horizontal))
                else:
                    break


def part1():
    grid = parse_input()

    d = find_shortest_path(grid, 0, 3, Vec(grid.shape[1] - 1, grid.shape[0] - 1))
    print(d)


def part2():
    grid = parse_input()

    d = find_shortest_path(grid, 4, 10, Vec(grid.shape[1] - 1, grid.shape[0] - 1))
    print(d)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
