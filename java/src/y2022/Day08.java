package y2022;


import utils.Matrix2d;
import utils.Point2d;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Stream;

public class Day08 {
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
        try (Stream<String> stream = Files.lines(Paths.get("inputs/08.txt"))) {
            var rows = stream.map(s -> s.chars().map(c -> c - '0').toArray()).toList();
            var matrix = rows.toArray(new int[rows.size()][rows.get(0).length]);
            return new Matrix2d(matrix);
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static void part1() {
        Matrix2d input = readInput();

        Matrix2d visibleMap = input.zerosLike();

        for (int y = 0; y < input.h; y++) {
            int hLast = -1;
            for (int x = 0; x < input.w; x++) {
                int h = input.get(x, y);
                if (h > hLast) {
                    visibleMap.set(x, y, 1);
                    hLast = h;
                }
            }
            hLast = -1;
            for (int x = input.w - 1; x >= 0; x--) {
                int h = input.get(x, y);
                if (h > hLast) {
                    visibleMap.set(x, y, 1);
                    hLast = h;
                }
            }
        }

        for (int x = 0; x < input.w; x++) {
            int hLast = -1;
            for (int y = 0; y < input.h; y++) {
                int h = input.get(x, y);
                if (h > hLast) {
                    visibleMap.set(x, y, 1);
                    hLast = h;
                }
            }
            hLast = -1;
            for (int y = input.h - 1; y >= 0; y--) {
                int h = input.get(x, y);
                if (h > hLast) {
                    visibleMap.set(x, y, 1);
                    hLast = h;
                }
            }
        }

        System.out.println(visibleMap.sum());
    }

    static void part2() {
        Matrix2d grid = readInput();

        int bestScore = 0;
        for (Point2d pos : grid.iterateCoords()) {
            int score = 1;
            for (Point2d dir : Point2d.ALL_DIRS) {
                Point2d p = pos.copy();
                final int h = grid.get(p);
                int c = 0;
                p.addI(dir);
                while (grid.isValidPosition(p)) {
                    c++;
                    if (grid.get(p) >= h) {
                        break;
                    }
                    p.addI(dir);
                }
                score *= c;
            }
            bestScore = Math.max(bestScore, score);

        }
        System.out.println(bestScore);
    }
}
