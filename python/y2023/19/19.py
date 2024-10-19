import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines()]

    sep = lines.index("")

    wfs = {}
    for l in lines[:sep]:
        rules = []
        name, rules_raw = l[:-1].split("{")
        for rule_raw in rules_raw.split(","):
            if ":" in rule_raw:
                cond_raw, out = rule_raw.split(":")
                gt = ">" in cond_raw
                var, val = cond_raw.split(">" if gt else "<")

                cond = (var, gt, int(val))
            else:
                out = rule_raw
                cond = None

            rules.append((out, cond))
        wfs[name] = rules

    parts = []
    for l in lines[sep + 1 :]:
        part = {}
        for var_raw in l[1:-1].split(","):
            var, val = var_raw.split("=")
            part[var] = int(val)
        parts.append(part)

    return wfs, parts


def part1():
    wfs, parts = parse_input()

    def check_part(part, wf):
        out = "A"
        for out, cond in wf:
            if cond is None:
                break

            var, gt, val = cond
            if gt:
                acc = part[var] > val
            else:
                acc = part[var] < val

            if acc:
                break

        if out == "A":
            return True
        elif out == "R":
            return False

        return check_part(part, wfs[out])

    total = 0
    for part in parts:
        if check_part(part, wfs["in"]):
            total += sum(part.values())

    print(total)


class Range:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __len__(self):
        return max(0, self.b - self.a)

    def __repr__(self):
        return f"Range({self.a}, {self.b})"


def part2():
    wfs, _ = parse_input()

    def find_solution_ranges(sol, wf_name):
        if wf_name == "A":
            return [sol]
        elif wf_name == "R":
            return []

        new_sols = []

        for out, cond in wfs[wf_name]:
            if cond is None:
                new_sols.extend(find_solution_ranges(sol, out))
                break

            var, gt, val = cond
            r = sol[var]

            if gt:
                r1, r2 = Range(val + 1, r.b), Range(r.a, val + 1)
            else:
                r1, r2 = Range(r.a, val), Range(val, r.b)

            if len(r1):
                new_sols.extend(find_solution_ranges({**sol, var: r1}, out))

            if len(r2):
                sol = {**sol, var: r2}
            else:
                break

        return new_sols

    sols_start = {
        "x": Range(1, 4001),
        "m": Range(1, 4001),
        "a": Range(1, 4001),
        "s": Range(1, 4001),
    }

    all_sols = find_solution_ranges(sols_start, "in")

    total = 0
    for sol in all_sols:
        subtotal = 1
        for r in sol.values():
            subtotal *= len(r)
        total += subtotal

    print(total)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
