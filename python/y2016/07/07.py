import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return [l.strip() for l in f.readlines() if l.strip()]


def supports_tls(ip):
    abba_outside = False
    abba_inside = False

    bracket = False
    for i in range(len(ip) - 3):
        if ip[i] == "[":
            bracket = True
        elif ip[i] == "]":
            bracket = False

        if ip[i] != ip[i + 1] and ip[i] == ip[i + 3] and ip[i + 1] == ip[i + 2]:
            if bracket:
                abba_inside = True
                break
            else:
                abba_outside = True
    return abba_outside and not abba_inside


def supports_ssl(ip):
    abas = set()
    babs = set()

    bracket = False
    for i in range(len(ip) - 2):
        if ip[i] == "[":
            bracket = True
        elif ip[i] == "]":
            bracket = False

        if ip[i] != ip[i + 1] and ip[i] == ip[i + 2]:
            if bracket:
                babs.add(ip[i : i + 3])
            else:
                abas.add(ip[i : i + 3])

    for aba in abas:
        bab = f"{aba[1]}{aba[0]}{aba[1]}"
        if bab in babs:
            return True

    return False


def part1():
    ips = parse_input()

    print(sum(1 for ip in ips if supports_tls(ip)))


def part2():
    ips = parse_input()

    print(sum(1 for ip in ips if supports_ssl(ip)))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
