import itertools
import math
import sys
from collections import defaultdict


def parse_input():
    debug = len(sys.argv) == 2 and sys.argv[1] == "debug"
    with open("debug.txt" if debug else "input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    ffs = {}
    cons = {}
    broadcast = []

    for line in lines:
        l, r = line.split(" -> ")
        outputs = r.split(", ")
        match l[0]:
            case "%":
                ffs[l[1:]] = outputs
            case "&":
                cons[l[1:]] = outputs
            case _:
                broadcast = outputs

    return broadcast, ffs, cons


def compute_con_ins(ffs, cons):
    con_ins = defaultdict(list)

    for k, outs in itertools.chain(ffs.items(), cons.items()):
        for out in outs:
            if out in cons:
                con_ins[out].append(k)

    return con_ins


LOW = False
HIGH = True


def part1():
    broadcast, ffs, cons = parse_input()
    con_ins = compute_con_ins(ffs, cons)

    state_ff = {k: LOW for k in ffs.keys()}
    state_con = {k: [LOW] * len(v) for k, v in con_ins.items()}

    def process_push(state_ff, state_con):
        lows = 1
        highs = 0
        queue = [("broadcast", LOW, broadcast)]
        while len(queue):
            sender, pulse, receivers = queue.pop(0)
            for receiver in receivers:
                # print(f"{sender} -{'high' if pulse else 'low'}-> {receiver}")
                if pulse == LOW:
                    lows += 1
                else:
                    highs += 1

                output_modules = []
                output_pulse = LOW

                if receiver in ffs and pulse == LOW:
                    output_modules = ffs[receiver]
                    state_ff[receiver] = not state_ff[receiver]
                    output_pulse = state_ff[receiver]
                elif receiver in cons:
                    output_modules = cons[receiver]
                    sender_idx = con_ins[receiver].index(sender)
                    state_con[receiver][sender_idx] = pulse
                    output_pulse = not all(state_con[receiver])

                queue.append((receiver, output_pulse, output_modules))

        return lows, highs

    lows_total = 0
    highs_total = 0
    for _ in range(1000):
        lows, highs = process_push(state_ff, state_con)
        lows_total += lows
        highs_total += highs

    print(lows_total * highs_total)


def plot_graph(broadcast, ffs, cons):
    import matplotlib.pyplot as plt
    import networkx as nx

    G = nx.DiGraph()

    for receiver in broadcast:
        G.add_edge("broadcast", receiver)

    for sender, receivers in ffs.items():
        for receiver in receivers:
            G.add_edge(sender, receiver)

    for sender, receivers in cons.items():
        for receiver in receivers:
            G.add_edge(sender, receiver)

    node_colors = []
    for node in G.nodes:
        if node == "broadcast":
            node_colors.append("red")
        elif node in ffs:
            node_colors.append("blue")
        elif node in cons:
            node_colors.append("green")
        else:
            node_colors.append("orange")

    # show graph
    nx.draw(G, with_labels=True, node_color=node_colors)
    plt.show()


def part2():
    broadcast, ffs, cons = parse_input()

    # plot_graph(broadcast, ffs, cons)

    # after plotting the graph, we can see that the graph is
    # split in 4 lanes that all end up in one conjunction that leads to rx
    # we can simulate the lanes separately and compute the lcm

    # lane 1: fv -> kz
    # lane 2: rt -> xj
    # lane 3: cr -> km
    # lane 4: tk -> qs

    def compute_subgraph(start, end):
        sub_ffs = {}
        sub_cons = {}
        q = [start]
        while q:
            node = q.pop(0)

            if node in ffs and not node in sub_ffs:
                if node == end:
                    sub_ffs[node] = []
                else:
                    sub_ffs[node] = ffs[node]
                    q.extend(ffs[node])
            if node in cons and not node in sub_cons:
                if node == end:
                    sub_cons[node] = []
                else:
                    sub_cons[node] = cons[node]
                    q.extend(cons[node])

        return sub_ffs, sub_cons

    def find_loop(start, end):
        ffs, cons = compute_subgraph(start, end)
        con_ins = compute_con_ins(ffs, cons)

        state_ff = {k: LOW for k in ffs.keys()}
        state_con = {k: [LOW] * len(v) for k, v in con_ins.items()}

        def process_push():
            queue = [("broadcast", LOW, [start])]
            while len(queue):
                sender, pulse, receivers = queue.pop(0)
                for receiver in receivers:
                    if receiver == end and pulse == LOW:
                        return True

                    output_modules = []
                    output_pulse = LOW

                    if receiver in ffs and pulse == LOW:
                        output_modules = ffs[receiver]
                        state_ff[receiver] = not state_ff[receiver]
                        output_pulse = state_ff[receiver]
                    elif receiver in cons:
                        output_modules = cons[receiver]
                        sender_idx = con_ins[receiver].index(sender)
                        state_con[receiver][sender_idx] = pulse
                        output_pulse = not all(state_con[receiver])

                    queue.append((receiver, output_pulse, output_modules))

            return False

        i = 1
        while not process_push():
            i += 1

        # we know that after the first pulse to the end node, the lane will loop
        # so we can just return the iteration count and stop the simulation

        return i

    lanes = [("fv", "kz"), ("rt", "xj"), ("cr", "km"), ("tk", "qs")]

    # find the lcm of the loop counts of the lanes
    lcm = math.lcm(*[find_loop(start, end) for start, end in lanes])

    print(lcm)


if __name__ == "__main__":
    print(">>> Part 1 <<<")
    part1()
    print("==============")
    print()
    print(">>> Part 2 <<<")
    part2()
    print("==============")
