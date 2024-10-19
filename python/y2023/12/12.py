import functools
import itertools
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    recs = []
    nss = []
    for line in lines:
        rec, ns = line.split(" ")
        ns = [int(n) for n in ns.split(",")]
        recs.append(rec)
        nss.append(ns)

    return recs, nss


def compute_solutions_brute_force(rec, ns):
    def check_rec(rec, ns):
        ni = 0
        acc = 0
        for c in itertools.chain(rec, "."):
            if c == "#":
                acc += 1
            elif c == "." and acc > 0:
                if acc != ns[ni]:
                    return False
                ni += 1
                acc = 0
        return ni == len(ns)

    sols = 0
    total_damaged = sum(ns)
    existing_damaged = rec.count("#")
    missing_i = [i for i, c in enumerate(rec) if c == "?"]
    missing_damaged = total_damaged - existing_damaged

    for damaged_indexes in itertools.combinations(missing_i, missing_damaged):
        new_rec = [c if c != "?" else "." for c in rec]
        for i in damaged_indexes:
            new_rec[i] = "#"
        if check_rec(new_rec, ns):
            sols += 1

    return sols


@functools.cache
def compute_solutions(rec, ns, inside):
    if len(rec) == 0:
        if sum(ns) == 0:
            return 1
        return 0

    c, rec = rec[0], rec[1:]

    if c == ".":
        if inside:
            if ns[0] != 0:
                return 0
            ns = ns[1:]
        return compute_solutions(rec, ns, False)
    elif c == "#":
        if not inside and len(ns) == 0:
            return 0
        n = ns[0] - 1
        if n < 0:
            return 0
        return compute_solutions(rec, (n, *ns[1:]), True)
    else:
        return compute_solutions("#" + rec, ns, inside) + compute_solutions("." + rec, ns, inside)


def part1():
    recs, nss = parse_input()

    total = 0
    for rec, ns in zip(recs, nss):
        total += compute_solutions_brute_force(rec, ns)

    print(total)


def part2():
    recs, nss = parse_input()

    for i, (rec, ns) in enumerate(zip(recs, nss)):
        recs[i] = "?".join([rec] * 5)
        nss[i] = ns * 5

    total = 0
    for rec, ns in zip(recs, nss):
        total += compute_solutions(rec, tuple(ns), False)
        # clear the cache after each call so it does not get too big
        compute_solutions.cache_clear()

    print(total)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
