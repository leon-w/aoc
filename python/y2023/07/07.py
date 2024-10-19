import itertools
import sys
from collections import Counter


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    hands = []
    bids = []

    for l in lines:
        hand, bid = l.split(" ", 1)
        hands.append(hand)
        bids.append(int(bid))

    return hands, bids


card_ranking = "AKQJT98765432"
card_ranking_j = "AKQT98765432J"


def compute_rank(hand):
    counts = Counter(hand).most_common()
    if counts[0][1] == 5:
        # five of a kind
        return 1
    elif counts[0][1] == 4:
        # four of a kind
        return 2
    elif len(counts) == 2:
        # full house
        return 3
    elif len(counts) == 3 and counts[0][1] == 3:
        # three of a kind
        return 4
    elif len(counts) == 3 and counts[0][1] == 2:
        # two pair
        return 5
    elif len(counts) == 4:
        # one pair
        return 6
    else:
        # high card
        return 7


def compute_rank_j(hand):
    js = [c == "J" for c in hand]

    jsc = sum(js)

    if jsc == 0:
        return compute_rank(hand)

    # brute force
    best_rank = 7
    for cs in itertools.product(card_ranking_j[:-1], repeat=jsc):
        new_hand = []
        ji = 0
        for i in range(len(hand)):
            if js[i]:
                new_hand.append(cs[ji])
                ji += 1
            else:
                new_hand.append(hand[i])
        best_rank = min(best_rank, compute_rank(new_hand))

    return best_rank


class Hand:
    def __init__(self, hand, j=False):
        self.hand = hand
        if j:
            self.t = compute_rank_j(hand)
            self.card_ranking = card_ranking_j
        else:
            self.t = compute_rank(hand)
            self.card_ranking = card_ranking

    def __repr__(self):
        return f"Hand('{self.hand}', t={self.t})"

    def __lt__(self, other):
        if self.t == other.t:
            for c1, c2 in zip(self.hand, other.hand):
                r1 = self.card_ranking.index(c1)
                r2 = self.card_ranking.index(c2)
                if r1 != r2:
                    return r1 > r2

        return self.t > other.t


def part1():
    hands, bids = parse_input()
    hands = list(map(lambda h: Hand(h), hands))
    rankings = sorted(zip(hands, bids), key=lambda x: x[0])

    points = 0
    for i, (_, bid) in enumerate(rankings):
        points += (i + 1) * bid

    print(f"Points: {points}")


def part2():
    hands, bids = parse_input()
    hands = list(map(lambda h: Hand(h, j=True), hands))
    rankings = sorted(zip(hands, bids), key=lambda x: x[0])

    points = 0
    for i, (_, bid) in enumerate(rankings):
        points += (i + 1) * bid

    print(f"Points: {points}")


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
