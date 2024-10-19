import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return f.read().strip()


forbidden = set(ord(c) - ord("a") for c in "iol")


def is_pw_valid(pw):
    if set(pw).intersection(forbidden):
        return False

    has_tri = False
    for i in range(len(pw) - 2):
        if pw[i] == pw[i + 1] - 1 == pw[i + 2] - 2:
            has_tri = True
            break

    if not has_tri:
        return False

    pairs = 0
    i = 0
    while i < len(pw) - 1:
        if pw[i] == pw[i + 1]:
            pairs += 1
            if pairs == 2:
                break
            i += 2
        else:
            i += 1

    return pairs == 2


def inc_pw(pw):
    for i in range(len(pw) - 1, -1, -1):
        carry, rest = divmod(pw[i] + 1, 26)
        pw[i] = rest
        if not carry:
            break


def find_next_password(pw):
    digits = [ord(c) - ord("a") for c in pw]
    while True:
        inc_pw(digits)
        if is_pw_valid(digits):
            break

    new_pw = "".join(chr(d + ord("a")) for d in digits)
    return new_pw


def part1():
    old_pw = parse_input()

    new_pw = find_next_password(old_pw)
    print(new_pw)


def part2():
    old_pw = parse_input()

    new_pw = find_next_password(old_pw)
    new_pw = find_next_password(new_pw)
    print(new_pw)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
