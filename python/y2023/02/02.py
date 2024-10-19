import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l]

    games = []
    for l in lines:
        game_id, parts = l.split(":")
        game_id = int(game_id.split(" ")[-1])
        parts = parts.split(";")

        parts_parsed = []
        for part in parts:
            colors = [0, 0, 0]
            segments = [s.strip() for s in part.split(",")]
            for segment in segments:
                n, c = segment.split(" ")
                n = int(n)
                if c == "red":
                    colors[0] = n
                elif c == "green":
                    colors[1] = n
                else:
                    colors[2] = n
            parts_parsed.append(colors)

        games.append((game_id, parts_parsed))

    return games


def part1():
    data = parse_input()

    id_sum = 0
    for game_id, parts in data:
        max_vals = [0, 0, 0]
        for part in parts:
            for i in range(3):
                max_vals[i] = max(max_vals[i], part[i])

        if max_vals[0] <= 12 and max_vals[1] <= 13 and max_vals[2] <= 14:
            id_sum += game_id

    print(f"Game ID sum: {id_sum}")


def part2():
    data = parse_input()

    power_sum = 0

    for _, parts in data:
        max_vals = [0, 0, 0]
        for part in parts:
            for i in range(3):
                max_vals[i] = max(max_vals[i], part[i])

        power = max_vals[0] * max_vals[1] * max_vals[2]

        power_sum += power

    print(f"Power sum: {power_sum}")


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")

    print(">>> Part 2 <<<")
    part2()
    print("==============")
