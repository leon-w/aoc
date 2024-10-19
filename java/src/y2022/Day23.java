package y2022;


import utils.Matrix2d;
import utils.Point2d;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.stream.Stream;

public class Day23 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static Matrix2d readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/23.txt"))) {
            int[][] data = stream.map(s -> s.chars().map(n -> n == '#' ? 1 : 0).toArray()).toArray(int[][]::new);
            return new Matrix2d(data);
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static int simulateElfs(Matrix2d map, int part) {
        Set<Point2d> elfs = new HashSet<>();
        for (Point2d pos : map.iterateCoords()) {
            if (map.get(pos) == 1) elfs.add(pos);

        }

        Point2d[][] directions = new Point2d[][]{
                {Point2d.NW, Point2d.N, Point2d.NE},
                {Point2d.SE, Point2d.S, Point2d.SW},
                {Point2d.SW, Point2d.W, Point2d.NW},
                {Point2d.NE, Point2d.E, Point2d.SE},
        };

        int round = 0;
        while (true) {
            Set<Point2d> allProposedSteps = new HashSet<>();
            Set<Point2d> bannedSteps = new HashSet<>();
            Map<Point2d, Point2d> nextSteps = new HashMap<>();

            for (Point2d elf : elfs) {
                boolean[] hasNeighbors = new boolean[4];
                Point2d nextPos = elf;

                // count neighbors
                for (int i = 0; i < 4; i++) {
                    for (Point2d direction : directions[i]) {
                        Point2d n = elf.add(direction);
                        if (elfs.contains(n)) {
                            hasNeighbors[i] = true;
                            break;
                        }
                    }
                }

                if (hasNeighbors[0] || hasNeighbors[1] || hasNeighbors[2] || hasNeighbors[3]) {
                    for (int i = 0; i < 4; i++) {
                        int idx = (i + round) % 4;
                        if (!hasNeighbors[idx]) {
                            nextPos = elf.add(directions[idx][1]);
                            break;
                        }
                    }
                }

                nextSteps.put(elf, nextPos);
                if (allProposedSteps.contains(nextPos)) {
                    bannedSteps.add(nextPos);
                }
                allProposedSteps.add(nextPos);
            }

            Set<Point2d> nextElfs = new HashSet<>();

            boolean changed = false;
            for (Point2d elf : elfs) {
                Point2d nextPos = nextSteps.get(elf);
                nextPos = bannedSteps.contains(nextPos) ? elf : nextPos;
                nextElfs.add(nextPos);
                if (!elf.equals(nextPos)) changed = true;
            }

            elfs = nextElfs;
            round++;

            if (part == 1 && round >= 10) break;
            if (part == 2 && !changed) break;
        }

        if (part == 1) {
            int minX = Integer.MAX_VALUE;
            int maxX = Integer.MIN_VALUE;
            int minY = Integer.MAX_VALUE;
            int maxY = Integer.MIN_VALUE;
            for (Point2d elf : elfs) {
                minX = Math.min(minX, elf.x);
                maxX = Math.max(maxX, elf.x);
                minY = Math.min(minY, elf.y);
                maxY = Math.max(maxY, elf.y);
            }

            int area = (maxX - minX + 1) * (maxY - minY + 1);
            return area - elfs.size();
        } else {
            return round;
        }
    }

    static void part1() {
        Matrix2d map = readInput();

        System.out.println(simulateElfs(map, 1));
    }

    static void part2() {
        Matrix2d map = readInput();

        System.out.println(simulateElfs(map, 2));
    }
}
