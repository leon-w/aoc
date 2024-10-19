from argparse import ArgumentParser
from pathlib import Path

import requests
from tqdm import tqdm

TEMPLATE = """
import sys


@@@PARSE@@@


def part1():
    data = parse_input()


def part2():
    data = parse_input()


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
"""

TEMPLATE_PARSE = """
def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    return lines
"""

TEMPLATE_PARSE_NUMBER = """
def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return int(f.read().strip())
"""

TEMPLATE_PARSE_LINE = """
def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        return f.read().strip()
"""


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("year", help="Year of the calendar")
    parser.add_argument("cookie", help="Session cookie to download the input")
    args = parser.parse_args()

    calendar_root = Path(args.year)
    calendar_root.mkdir(exist_ok=True)

    for day in tqdm(range(1, 26)):
        r = requests.get(f"https://adventofcode.com/{args.year}/day/{day}/input", cookies={"session": args.cookie})
        if r.status_code == 404:
            break

        if not r.ok:
            r.raise_for_status()

        puzzle_input = r.text.strip()

        day_folder = calendar_root / f"{day:02}"
        day_folder.mkdir(exist_ok=True)

        script = day_folder / f"{day:02}.py"
        if not script.exists():
            with open(script, "w") as f:
                parse_template = TEMPLATE_PARSE if "\n" in puzzle_input else TEMPLATE_PARSE_LINE
                try:
                    int(puzzle_input)
                    parse_template = TEMPLATE_PARSE_NUMBER
                except ValueError:
                    pass

                f.write(TEMPLATE.replace("@@@PARSE@@@", parse_template.strip()).lstrip())

        input_file = day_folder / "input.txt"
        if not input_file.exists():
            with open(input_file, "w") as f:
                f.write(r.text)
