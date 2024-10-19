import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    reindeer = []

    for line in lines:
        parts = line.split(" ")
        speed = int(parts[3])
        dur = int(parts[6])
        rest = int(parts[-2])
        reindeer.append((speed, dur, rest))

    return reindeer


def compute_reindeer_distance(reindeer, time):
    speed, dur, rest = reindeer

    cycle_len = dur + rest
    cycle, rem = divmod(time, cycle_len)

    return cycle * speed * dur + speed * min(rem, dur)


def part1():
    reindeer = parse_input()

    max_dist = max(compute_reindeer_distance(r, 2503) for r in reindeer)
    print(max_dist)


def part2():
    reindeer = parse_input()

    points = [0] * len(reindeer)

    for t in range(1, 2504):
        dists = [compute_reindeer_distance(r, t) for r in reindeer]
        max_dist = max(dists)
        for i in range(len(reindeer)):
            if dists[i] == max_dist:
                points[i] += 1

    print(max(points))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
