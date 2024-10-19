package y2022;


import utils.Matrix2d;
import utils.Point2d;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.stream.Stream;

public class Day14 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static List<List<Point2d>> readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/14.txt"))) {
            return stream.map(s -> Arrays.stream(s.split(" -> ")).map(p -> {
                String[] parts = p.split(",");
                return new Point2d(Integer.parseInt(parts[0]), Integer.parseInt(parts[1]));
            }).toList()).toList();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static RockMap prepareRockMap(List<List<Point2d>> rocks, int padBottom) {
        Point2d min = new Point2d(Integer.MAX_VALUE, Integer.MAX_VALUE);
        Point2d max = new Point2d(Integer.MIN_VALUE, Integer.MIN_VALUE);
        rocks.stream().flatMap(Collection::stream).forEach(p -> {
            min.x = Math.min(min.x, p.x);
            min.y = Math.min(min.y, p.y);
            max.x = Math.max(max.x, p.x);
            max.y = Math.max(max.y, p.y);
        });

        rocks.stream().flatMap(Collection::stream).forEach(p -> p.x -= min.x);

        Matrix2d m = new Matrix2d(max.x - min.x + 1, max.y + 1 + padBottom);

        for (List<Point2d> rock : rocks) {
            for (int i = 0; i < rock.size() - 1; i++) {
                Point2d a = rock.get(i);
                Point2d b = rock.get(i + 1);

                int distX = b.x - a.x;
                int dX = distX > 0 ? 1 : -1;
                for (int x = 0; x < Math.abs(distX) + 1; x++) {
                    m.set(a.x + dX * x, a.y, 1);
                }

                int distY = b.y - a.y;
                int dY = distY > 0 ? 1 : -1;
                for (int y = 0; y < Math.abs(distY) + 1; y++) {
                    m.set(a.x, a.y + dY * y, 1);
                }
            }
        }

        return new RockMap(m, min.x);
    }

    static void part1() {
        List<List<Point2d>> rocks = readInput();

        RockMap rm = prepareRockMap(rocks, 0);

        placeSand:
        while (true) {
            Point2d p = new Point2d(500 - rm.offsetX, 0);
            while (true) {
                p.addI(Point2d.DOWN);
                if (rm.map.isValidPosition(p)) {
                    if (rm.map.get(p) == 0) {
                        continue;
                    }
                } else {
                    // out of bounds
                    break placeSand;
                }
                p.addI(Point2d.LEFT);
                if (rm.map.isValidPosition(p)) {
                    if (rm.map.get(p) == 0) {
                        continue;
                    }
                } else {
                    // out of bounds
                    break placeSand;
                }
                p.addI(Point2d.RIGHT);
                p.addI(Point2d.RIGHT);
                if (rm.map.isValidPosition(p)) {
                    if (rm.map.get(p) == 0) {
                        continue;
                    }
                } else {
                    // out of bounds
                    break placeSand;
                }

                // undo movement
                p.addI(Point2d.UP);
                p.addI(Point2d.LEFT);

                // sand placed
                rm.map.set(p, 2);
                break;
            }
        }

        //        System.out.println(rm.map.toString(d -> switch (d) {
        //            case 0 -> ".";
        //            case 1 -> "#";
        //            case 2 -> "o";
        //            default -> "?";
        //        }));

        int sandCount = rm.map.count(2);
        System.out.println(sandCount);
    }

    static void part2() {
        List<List<Point2d>> rocks = readInput();

        RockMap rm = prepareRockMap(rocks, 1);

        // mark all unreachable positions
        for (int y = 1; y < rm.map.h; y++) {
            for (int x = 1; x < rm.map.w - 1; x++) {
                if (rm.map.get(x - 1, y - 1) == 1 && rm.map.get(x, y - 1) == 1 && rm.map.get(x + 1, y - 1) == 1) {
                    rm.map.set(x, y, 1);
                }
            }
        }

        //        System.out.println(rm.map.toString(d -> switch (d) {
        //            case 0 -> ".";
        //            case 1 -> "#";
        //            case 2 -> "o";
        //            default -> "?";
        //        }));

        int blocked = rm.map.count(1);
        int maxSand = rm.map.h * rm.map.h;
        int sandCount = maxSand - blocked;

        System.out.println(sandCount);
    }

    record RockMap(Matrix2d map, int offsetX) {}
}
