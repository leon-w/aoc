import itertools
import re
import sys
from functools import cache

import numpy as np


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    materials = ["hydrogen", "lithium"] if debug else ["strontium", "plutonium", "thulium", "ruthenium", "curium"]

    chips = [[0] * len(materials) for _ in range(4)]
    generators = [[0] * len(materials) for _ in range(4)]

    for i, line in enumerate(lines):
        for m in re.findall(r"(\w+)-compatible", line):
            chips[i][materials.index(m)] = 1
        for m in re.findall(r"(\w+) generator", line):
            generators[i][materials.index(m)] = 1

    return np.array(chips, dtype=np.int8), np.array(generators, dtype=np.int8)


class GameState:
    def __init__(self, elevator, chips, generators):
        self.elevator = elevator
        self.chips = chips
        self.generators = generators

    def __hash__(self):
        return hash((self.elevator, tuple(self.chips.flatten()), tuple(self.generators.flatten())))

    def __eq__(self, other):

        return (
            self.elevator == other.elevator
            and np.all(self.chips == other.chips)
            and np.all(self.generators == other.generators)
        )

    def is_valid(self):
        return not np.any(self.generators.sum(axis=1) & (self.chips - self.generators).clip(min=0).sum(axis=1))

    def clone(self):
        return GameState(self.elevator, self.chips.copy(), self.generators.copy())

    def generate_moves(self):
        directions = []
        if self.elevator > 0:
            directions.append(-1)
        if self.elevator < 3:
            directions.append(1)

        for d in directions:
            for a in [1, 2]:

                (i_chips,) = np.nonzero(self.chips[self.elevator])
                (i_generators,) = np.nonzero(self.generators[self.elevator])

                i_chips = tuple(("c", i) for i in i_chips)
                i_generators = tuple(("g", i) for i in i_generators)

                for combo in itertools.combinations(i_chips + i_generators, a):
                    new_state = self.clone()
                    new_state.elevator += d
                    for t, i in combo:
                        if t == "c":
                            new_state.chips[self.elevator][i] -= 1
                            new_state.chips[self.elevator + d][i] += 1
                        elif t == "g":
                            new_state.generators[self.elevator][i] -= 1
                            new_state.generators[self.elevator + d][i] += 1
                    if new_state.is_valid():
                        yield new_state


@cache
def find_least_steps(state):
    # pairs = (state.chips == state.generators) & (state.chips == 1)

    # keep = np.array([True, False, True, True, False])

    # state.chips = state.chips[:, keep]
    # state.generators = state.generators[:, keep]

    # extra_steps = 0

    q = [(0, state)]

    visited = set()
    visited.add(state)

    max_steps = 0

    while len(q) > 0:
        steps, state = q.pop(0)
        if np.all(state.chips[-1]) and np.all(state.generators[-1]) and state.elevator == 3:
            return steps

        if steps > max_steps:
            max_steps = steps
            print(max_steps, len(visited))

        for new_state in state.generate_moves():
            if new_state not in visited:
                visited.add(new_state)
                q.append((steps + 1, new_state))

    raise Exception("No solution found")


def part1():
    chips, generators = parse_input()

    print(find_least_steps(GameState(0, chips, generators)))


def part2():
    chips, generators = parse_input()

    print(find_least_steps(GameState(0, chips, generators)) + 12)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
