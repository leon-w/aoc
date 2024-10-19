import sys
from collections import Counter


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    rooms = []
    for line in lines:
        cipher, r = line.rsplit("-", maxsplit=1)
        sector_id = int(r[:-7])
        checksum = r[-6:-1]
        rooms.append((cipher, sector_id, checksum))

    return rooms


def part1():
    rooms = parse_input()

    total = 0
    for cipher, sector_id, checksum in rooms:
        counter = Counter(sorted(cipher.replace("-", "")))
        computed_checksum = "".join(c for c, _ in counter.most_common(5))
        if computed_checksum == checksum:
            total += sector_id

    print(total)


def part2():
    rooms = parse_input()

    ord_a = ord("a")

    for cipher, sector_id, _ in rooms:
        text = []
        for c in cipher:
            if c == "-":
                text.append(" ")
            else:
                text.append(chr(((ord(c) - ord_a + sector_id) % 26) + ord_a))
        if "".join(text) == "northpole object storage":
            print(sector_id)
            break


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
