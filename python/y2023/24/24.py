import itertools
import sys

import numpy as np
import z3


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    hailstones = []

    def parse_vector(s):
        return list(map(int, s.split(", ")))

    for line in lines:
        l, r = line.split(" @ ")
        hailstones.append((parse_vector(l), parse_vector(r)))

    return hailstones


def part1():
    hailstones = parse_input()

    # we will process all pairs at once using numpy as it is the fastest method

    bases1 = []
    bases2 = []
    dirs1 = []
    dirs2 = []

    for (base1, direction1), (base2, direction2) in itertools.combinations(hailstones, 2):
        bases1.append(base1[:2])
        bases2.append(base2[:2])
        dirs1.append(direction1[:2])
        dirs2.append(direction2[:2])

    bases1 = np.array(bases1)
    bases2 = np.array(bases2)
    dirs1 = np.array(dirs1)
    dirs2 = np.array(dirs2)

    A = np.empty((len(bases1), 2, 2), dtype=bases1.dtype)
    A[:, :, 0] = dirs1
    A[:, :, 1] = -dirs2
    b = bases2 - bases1

    solvable = np.linalg.matrix_rank(A) == 2

    A = A[solvable]
    b = b[solvable]
    bases1 = bases1[solvable]
    bases2 = bases2[solvable]
    dirs1 = dirs1[solvable]
    dirs2 = dirs2[solvable]

    t1, t2 = np.linalg.solve(A, b).T

    valid = (t1 >= 0) & (t2 >= 0)

    bases1 = bases1[valid]
    bases2 = bases2[valid]
    dirs1 = dirs1[valid]
    dirs2 = dirs2[valid]

    t1 = t1[valid]
    t2 = t2[valid]

    p = bases1 + t1[:, None] * dirs1

    valid = (200000000000000 <= p) & (p <= 400000000000000)

    print((valid.sum(axis=1) == 2).sum())


def part2():
    hailstones = parse_input()

    solver = z3.Solver()

    t = z3.IntVector("t", 3)
    a = z3.IntVector("a", 3)
    b = z3.IntVector("b", 3)

    for i, (h_a, h_b) in enumerate(hailstones[:3]):
        for d in range(3):
            solver.add(h_a[d] + t[i] * h_b[d] == a[d] + t[i] * b[d])

    if solver.check() == z3.sat:
        model = solver.model()
        print(model.eval(a[0] + a[1] + a[2]))
    else:
        print("ERROR SOLVING")


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
