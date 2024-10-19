import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        data = f.read().strip()

    return data.split(",")


def HASH(string):
    x = 0
    for c in string:
        x += ord(c)
        x *= 17
        x %= 256
    return x


def part1():
    data = parse_input()

    total = 0
    for part in data:
        total += HASH(part)

    print(total)


def part2():
    data = parse_input()

    hashmap = {}
    for part in data:
        if "-" in part:
            label = part[:-1]
            label_hash = HASH(label)
            if label_hash in hashmap:
                labels, fs = hashmap[label_hash]
                if label in labels:
                    i = labels.index(label)
                    del labels[i], fs[i]
        if "=" in part:
            label = part[:-2]
            label_hash = HASH(label)
            f = int(part[-1])
            if label_hash not in hashmap:
                hashmap[label_hash] = ([], [])
            labels, fs = hashmap[label_hash]
            if label in labels:
                fs[labels.index(label)] = f
            else:
                labels.append(label)
                fs.append(f)

    total = 0
    for h, (_, fs) in hashmap.items():
        for i, f in enumerate(fs):
            total += (h + 1) * (i + 1) * f

    print(total)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
