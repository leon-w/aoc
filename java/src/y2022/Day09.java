package y2022;


import utils.Point2d;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Stream;


public class Day09 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static List<Move> readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/09.txt"))) {
            return stream.map(s -> {
                String[] parts = s.split(" ");
                Point2d d = switch (parts[0]) {
                    case "U" -> Point2d.UP;
                    case "D" -> Point2d.DOWN;
                    case "L" -> Point2d.LEFT;
                    case "R" -> Point2d.RIGHT;
                    default -> throw new IllegalArgumentException("Invalid direction");
                };
                return new Move(d, Integer.parseInt(parts[1]));
            }).toList();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static int simulateRope(List<Move> moves, int ropeLen) {
        Point2d[] knots = new Point2d[ropeLen];
        for (int i = 0; i < ropeLen; i++) {
            knots[i] = new Point2d(0, 0);
        }

        Set<Point2d> visited = new HashSet<>();
        for (Move move : moves) {
            for (int step = 0; step < move.steps; step++) {
                knots[0].addI(move.direction);
                for (int i = 0; i < ropeLen - 1; i++) {
                    Point2d h = knots[i];
                    Point2d t = knots[i + 1];

                    int dX = h.x - t.x;
                    int dY = h.y - t.y;

                    boolean changed = false;
                    if (Math.abs(dX) == 2) {
                        t.x += dX / 2;
                        if (Math.abs(dY) == 1) {
                            t.y += dY;
                        }
                        changed = true;
                    }
                    if (Math.abs(dY) == 2) {
                        t.y += dY / 2;
                        if (Math.abs(dX) == 1) {
                            t.x += dX;
                        }
                        changed = true;
                    }

                    if (!changed) {
                        break;
                    }
                }
                visited.add(knots[ropeLen - 1].copy());
            }

        }

        return visited.size();
    }

    static void part1() {
        List<Move> moves = readInput();

        System.out.println(simulateRope(moves, 2));
    }

    static void part2() {
        List<Move> moves = readInput();

        System.out.println(simulateRope(moves, 10));
    }

    record Move(Point2d direction, int steps) {}
}
