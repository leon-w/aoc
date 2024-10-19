import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return int(f.read().strip())


def is_wall(x, y, n):
    w = x * x + 3 * x + 2 * x * y + y + y * y + n
    return bin(w).count("1") % 2 == 1


def part1():
    n = parse_input()

    target_x, target_y = 31, 39

    queue = [(0, 1, 1)]
    visited = set()

    while len(queue):
        l, x, y = queue.pop(0)

        if x == target_x and y == target_y:
            print(l)
            break

        visited.add((x, y))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            xn = x + dx
            yn = y + dy

            if xn >= 0 and yn >= 0 and not (xn, yn) in visited and not is_wall(xn, yn, n):
                queue.append((l + 1, xn, yn))


def part2():
    n = parse_input()

    queue = [(0, 1, 1)]
    visited = set()

    while len(queue):
        l, x, y = queue.pop(0)

        if l > 50:
            print(len(visited))
            break

        visited.add((x, y))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            xn = x + dx
            yn = y + dy

            if xn >= 0 and yn >= 0 and not (xn, yn) in visited and not is_wall(xn, yn, n):
                queue.append((l + 1, xn, yn))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
