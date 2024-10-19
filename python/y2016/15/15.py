import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    disks = []
    for line in lines:
        parts = line.split(" ")
        disks.append((int(parts[3]), int(parts[-1][:-1])))

    return disks


def find_time(disks):
    t = 0
    while True:
        works = True
        for i, (s, p) in enumerate(disks):
            if (t + i + p + 1) % s != 0:
                works = False
                break

        if works:
            return t

        t += 1


def part1():
    disks = parse_input()

    print(find_time(disks))


def part2():
    disks = parse_input()

    disks.append((11, 0))

    print(find_time(disks))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
