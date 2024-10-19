import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    seeds = [int(s) for s in lines.pop(0).split(": ")[-1].split(" ")]

    maps = []

    for line in lines:
        if line[-1] == ":":
            maps.append([])
        else:
            start_out, start_in, length = map(int, line.split(" "))
            maps[-1].append((Range(start_in, length), start_out - start_in))

    return seeds, maps


class Range:
    def __init__(self, start, length):
        self.s = start
        self.l = length
        self.e = start + length - 1

    def shift(self, amount):
        return Range(self.s + amount, self.l)

    def __contains__(self, n):
        return n >= self.s and n <= self.e

    def __repr__(self):
        return f"<{self.s}/{self.e}|{self.l}>"


def part1():
    seeds, mappings = parse_input()

    def apply_mapping(x, mapping):
        for r, shift in mapping:
            if x in r:
                return x + shift
        return x

    def apply_mapping_multi(x, mappings):
        for mapping in mappings:
            x = apply_mapping(x, mapping)
        return x

    locations = [apply_mapping_multi(seed, mappings) for seed in seeds]

    print(f"Smallest location: {min(locations)}")


def part2():
    seeds, mappings = parse_input()

    seed_ranges = [Range(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]

    def apply_mapping_range(rin, mapping):
        for r, shift in mapping:
            if rin.s in r and rin.e in r:
                # fully inside
                return [rin.shift(shift)]
            elif rin.e in r and rin.s not in r:
                # overlapping left
                l1, l2 = r.s - rin.s, rin.e - r.s
                r1 = Range(rin.s, l1)
                r2 = Range(r.s + 1, l2)
                return apply_mapping_range(r1, mapping) + [r2.shift(shift)]
            elif rin.s in r and rin.e not in r:
                # overlapping right
                l1, l2 = r.e - rin.s, rin.e - r.e
                r1 = Range(rin.s, l1 + 1)
                r2 = Range(r.e + 1, l2)
                return [r1.shift(shift)] + apply_mapping_range(r2, mapping)
            elif r.s in rin and r.e in rin:
                # enclosing
                l1, l2 = r.s - rin.s, rin.e - r.e
                r1 = Range(rin.s, l1)
                r2 = Range(r.e + 1, l2 - 1)
                return apply_mapping_range(r1, mapping) + [r.shift(shift)] + apply_mapping_range(r2, mapping)
        return [rin]

    def apply_mappings_multi_range(ra, mappings):
        ras = [ra]
        for mapping in mappings:
            new_ras = []
            for ra in ras:
                new_ras.extend(apply_mapping_range(ra, mapping))
            ras = new_ras

        return ras

    all_outputs = []
    for sr in seed_ranges:
        all_outputs.extend(apply_mappings_multi_range(sr, mappings))

    min_loc = min(map(lambda r: r.s, all_outputs))

    print(f"Smallest location: {min_loc}")


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
