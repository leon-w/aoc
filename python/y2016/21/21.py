import re
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return [l.strip() for l in f.readlines() if l.strip()]


def scramble(pw, instructions):
    pw = list(pw)

    for ins in instructions:
        if m := re.match(r"swap position (\d+) with position (\d+)", ins):
            x, y = map(int, m.groups())
            pw[x], pw[y] = pw[y], pw[x]
        elif m := re.match(r"swap letter ([a-zA-Z]) with letter ([a-zA-Z])", ins):
            lx, ly = m.groups()
            x, y = pw.index(lx), pw.index(ly)
            pw[x], pw[y] = pw[y], pw[x]
        elif m := re.match(r"rotate (left|right) (\d+) steps?", ins):
            d, x = m.groups()
            x = int(x) % len(pw)
            if d == "left":
                x = len(pw) - x
            pw = pw[len(pw) - x :] + pw[: len(pw) - x]
        elif m := re.match(r"rotate based on position of letter ([a-zA-Z])", ins):
            l = m.group(1)
            x = pw.index(l) + 1
            if x > 4:
                x += 1
            x %= len(pw)
            pw = pw[len(pw) - x :] + pw[: len(pw) - x]
        elif m := re.match(r"reverse positions (\d+) through (\d+)", ins):
            x, y = map(int, m.groups())
            pw[x : y + 1] = pw[x : y + 1][::-1]
        elif m := re.match(r"move position (\d+) to position (\d+)", ins):
            x, y = map(int, m.groups())
            l = pw[x]
            del pw[x]
            pw.insert(y, l)
        else:
            print("! invalid instruction:", ins)

    return "".join(pw)


def unscramble(pw, instructions):
    pw = list(pw)

    for ins in instructions[::-1]:
        if m := re.match(r"swap position (\d+) with position (\d+)", ins):
            x, y = map(int, m.groups())
            pw[x], pw[y] = pw[y], pw[x]
        elif m := re.match(r"swap letter ([a-zA-Z]) with letter ([a-zA-Z])", ins):
            lx, ly = m.groups()
            x, y = pw.index(lx), pw.index(ly)
            pw[x], pw[y] = pw[y], pw[x]
        elif m := re.match(r"rotate (left|right) (\d+) steps?", ins):
            d, x = m.groups()
            x = int(x) % len(pw)
            if d == "right":
                x = len(pw) - x
            pw = pw[len(pw) - x :] + pw[: len(pw) - x]
        elif m := re.match(r"rotate based on position of letter ([a-zA-Z])", ins):
            l = m.group(1)
            i = pw.index(l)
            x = {1: 1, 3: 2, 5: 3, 7: 4, 2: 6, 4: 7, 6: 0, 0: 1}[i]
            x = len(pw) - x
            pw = pw[len(pw) - x :] + pw[: len(pw) - x]
        elif m := re.match(r"reverse positions (\d+) through (\d+)", ins):
            x, y = map(int, m.groups())
            pw[x : y + 1] = pw[x : y + 1][::-1]
        elif m := re.match(r"move position (\d+) to position (\d+)", ins):
            x, y = map(int, m.groups())
            l = pw[y]
            del pw[y]
            pw.insert(x, l)
        else:
            print("invalid instruction:", ins)

    return "".join(pw)


def part1():
    instructions = parse_input()

    print(scramble("abcdefgh", instructions))


def part2():
    instructions = parse_input()

    pw = "fbgdceah"

    print(unscramble(pw, instructions))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
