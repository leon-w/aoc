package y2022;


import utils.Matrix2d;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

public class Day16 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static List<ValveNode> readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/16.txt"))) {
            Pattern pattern = Pattern.compile("Valve ([A-Z]+) has flow rate=(\\d+); tunnels? leads? to valves? (([A-Z]+, )*[A-Z]+)");
            return stream.map(pattern::matcher)
                    .filter(Matcher::matches)
                    .map(m -> new ValveNode(m.group(1), Integer.parseInt(m.group(2)), m.group(3).split(", ")))
                    .toList();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static void part1() {
        List<ValveNode> nodes = readInput();

        FlowOptimizer optimizer = new FlowOptimizer(nodes);

        long startTime = System.currentTimeMillis();

        int maxFlow = optimizer.optimizeFlow(optimizer.start, optimizer.nonZero, 30);

        long executionTime = System.currentTimeMillis() - startTime;
        System.out.printf("Execution took %dms\n", executionTime);

        System.out.println(maxFlow);
    }

    static void part2() {
        List<ValveNode> nodes = readInput();

        FlowOptimizer optimizer = new FlowOptimizer(nodes);

        long startTime = System.currentTimeMillis();

        int maxFlow = 0;
        int maxVal = (0b1 << optimizer.nodeCount - 1) - 1;
        for (int i = 0; i < maxVal / 2 + 1; i++) {
            int left = i << 1;
            int right = (maxVal - i) << 1;
            int flowLeft = optimizer.optimizeFlow(optimizer.start, left, 26);
            int flowRight = optimizer.optimizeFlow(optimizer.start, right, 26);
            maxFlow = Math.max(maxFlow, flowLeft + flowRight);
        }

        long executionTime = System.currentTimeMillis() - startTime;
        System.out.printf("Execution took %dms\n", executionTime);

        System.out.println(maxFlow);
    }

    static class FlowOptimizer {
        final int start;
        final int nonZero;
        final int nodeCount;
        private final int[] flows;
        private final int nodeIndexBitCount;
        private final int timeBitCount;

        private final int[] cache;

        private final Matrix2d shortestDistances;

        public FlowOptimizer(List<ValveNode> rawNodes) {
            ValveNode startNode = rawNodes.stream().filter(n -> n.name.equals("AA")).findFirst().orElseThrow();
            List<ValveNode> nonZeroNodes = rawNodes.stream().filter(n -> n.flow > 0).toList();

            List<ValveNode> allNodes = new ArrayList<>();
            allNodes.add(startNode);
            allNodes.addAll(nonZeroNodes);
            shortestDistances = computeDistanceMatrix(allNodes, rawNodes);

            flows = allNodes.stream().mapToInt(n -> n.flow).toArray();

            nodeCount = allNodes.size();
            nodeIndexBitCount = countRequiredBits(allNodes.size());
            timeBitCount = countRequiredBits(30);

            cache = new int[0b1 << (nodeCount + nodeIndexBitCount + timeBitCount)];
            Arrays.fill(cache, -1);

            start = 0;
            nonZero = (0b1 << nodeCount) - 2;
        }

        private static int countRequiredBits(int n) {
            int count = 0;
            for (n = Integer.highestOneBit(n); n > 0; n >>= 1) {
                count++;
            }
            return count;
        }

        private static Matrix2d computeDistanceMatrix(List<ValveNode> relevantNodes, List<ValveNode> rawNodes) {
            Map<String, ValveNode> nodeMap = new HashMap<>();
            rawNodes.forEach(n -> nodeMap.put(n.name, n));

            Matrix2d shortestDistances = new Matrix2d(relevantNodes.size(), relevantNodes.size());
            record NodeWithDistance(ValveNode node, int d) {}
            for (int iSource = 0; iSource < relevantNodes.size(); iSource++) {
                Set<String> visited = new HashSet<>();
                Queue<NodeWithDistance> q = new LinkedList<>();
                q.add(new NodeWithDistance(relevantNodes.get(iSource), 0));
                while (!q.isEmpty()) {
                    NodeWithDistance entry = q.poll();
                    ValveNode currentNode = entry.node;
                    int d = entry.d;

                    if (visited.contains(currentNode.name)) continue;
                    visited.add(currentNode.name);

                    int iTarget = relevantNodes.indexOf(currentNode);
                    if (iTarget >= 0) {
                        shortestDistances.set(iSource, iTarget, d);
                    }

                    for (String neighbor : currentNode.connections) {
                        q.add(new NodeWithDistance(nodeMap.get(neighbor), d + 1));
                    }
                }
            }

            return shortestDistances;
        }

        private int getCacheAddress(int startNode, int remainingNodes, int remainingTime) {
            return (((remainingNodes << nodeIndexBitCount) | startNode) << timeBitCount) | remainingTime;
        }

        public int optimizeFlow(int startNode, int remainingNodes, int remainingTime) {
            int id = getCacheAddress(startNode, remainingNodes, remainingTime);
            int cacheVal = cache[id];
            if (cacheVal != -1) return cacheVal;

            if (remainingTime <= 0) return 0;

            int flow = flows[startNode] * remainingTime;
            int maxNextFlow = 0;

            for (int x = remainingNodes, i = 0; x > 0; i++, x >>= 1) {
                if ((x & 0b1) == 1) {
                    int nextRemainingNodes = remainingNodes & ~(0b1 << i);
                    int nextRemainingTime = remainingTime - shortestDistances.get(startNode, i) - 1;
                    if (nextRemainingTime <= 0) continue;

                    int nextFlow = optimizeFlow(i, nextRemainingNodes, nextRemainingTime);
                    maxNextFlow = Math.max(maxNextFlow, nextFlow);
                }
            }

            flow += maxNextFlow;
            cache[id] = flow;

            return flow;
        }
    }

    record ValveNode(String name, int flow, String[] connections) {}
}
