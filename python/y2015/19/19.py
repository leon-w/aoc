import random
import sys


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    rules = []
    for line in lines[:-1]:
        l, r = line.split(" => ")
        rules.append((l, r))

    return rules, lines[-1]


def find_positions(pattern, s):
    lp = len(pattern)
    for i in range(len(s) - len(pattern) + 1):
        if s[i : i + lp] == pattern:
            yield i


def includes(pattern, s):
    try:
        next(find_positions(pattern, s))
        return True
    except StopIteration:
        return False


def split_elements(s):
    elements = []
    last = 0
    for i in range(1, len(s)):
        if s[i].upper() == s[i]:
            elements.append(s[last:i])
            last = i
    elements.append(s[last:])
    return elements


def find_min_replacements_random(rules, seq, total_candidates=10):
    targets = [split_elements(r[1]) for r in rules if r[0] == "e"]
    max_len = max(len(t) for t in targets)

    rules = [(l, split_elements(r)) for l, r in rules if l != "e"]
    seq = list(split_elements(seq))

    candidates = []

    while total_candidates > 0:
        seq_copy = seq.copy()
        failed = False

        num_replacements = 1  # 1 for the transition to e that we omit here
        while len(seq_copy) > max_len or seq_copy not in targets:
            possible_rules = [r for r in rules if includes(r[1], seq_copy)]

            if len(possible_rules) == 0:
                failed = True
                break

            rule = random.choice(possible_rules)
            position = random.choice(list(find_positions(rule[1], seq_copy)))

            del seq_copy[position : position + len(rule[1])]
            seq_copy.insert(position, rule[0])
            num_replacements += 1

        if not failed:
            total_candidates -= 1
            candidates.append(num_replacements)

    return min(candidates)


def part1():
    rules, seq = parse_input()

    results = set()

    for pattern, replacement in rules:
        for i in find_positions(pattern, seq):
            results.add(f"{seq[: i]}{replacement}{seq[i + len(pattern) :]}")

    print(len(results))


def part2():
    rules, seq = parse_input()

    # in theory this could work but in practice it's too slow
    """
    import nltk

    start = "e"
    nts = {nt: nltk.grammar.Nonterminal(nt) for nt in set(l for l, _ in rules)}
    productions = []

    for nt in nts.keys():
        productions.append(nltk.grammar.Production(nts[nt], [nt]))

    for lhs, rhs in rules:
        productions.append(nltk.grammar.Production(nts[lhs], [nts[r] if r in nts else r for r in split_elements(rhs)]))

    g = nltk.grammar.CFG(nts[start], productions)
    parser = nltk.parse.EarleyChartParser(g)

    for tree in parser.parse(split_elements(seq)):
        print(len(tree.productions()))
        break
    """

    print(find_min_replacements_random(rules, seq))


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
