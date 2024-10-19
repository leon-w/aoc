package y2022;


import utils.Matrix2d;
import utils.Point2d;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Stream;

public class Day24 {
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
        try (Stream<String> stream = Files.lines(Paths.get("inputs/24.txt"))) {
            int[][] data = stream.map(s -> s.chars().map(x -> switch (x) {
                case '^' -> 0b00001;
                case '>' -> 0b00010;
                case 'v' -> 0b00100;
                case '<' -> 0b01000;
                case '#' -> 0b10000;
                default -> 0;
            }).toArray()).toArray(int[][]::new);

            return new Matrix2d(data);
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }


    static void part1() {
        Matrix2d map = readInput();

        BlizzardMap bm = new BlizzardMap(map);

        int t = bm.findShortestDistance(bm.start, bm.end, 0);

        System.out.println(t);
    }

    static void part2() {
        Matrix2d map = readInput();

        BlizzardMap bm = new BlizzardMap(map);

        int t1 = bm.findShortestDistance(bm.start, bm.end, 0);
        int t2 = bm.findShortestDistance(bm.end, bm.start, t1);
        int t3 = bm.findShortestDistance(bm.start, bm.end, t2);

        System.out.println(t3);
    }

    static class BlizzardMap {
        List<Matrix2d> mapOverTime;
        Point2d start;
        Point2d end;

        BlizzardMap(Matrix2d map) {
            mapOverTime = new ArrayList<>();
            mapOverTime.add(map);
            start = new Point2d(1, 0);
            end = new Point2d(map.w - 2, map.h - 1);
        }

        static Matrix2d simulateStep(Matrix2d current) {
            Matrix2d next = current.zerosLike();

            final int w = current.w;
            final int h = current.h;

            for (int x = 0; x < w; x++) {
                for (int y = 0; y < h; y++) {
                    int val = current.get(x, y);
                    if (val > 0) {
                        // ^
                        if ((val & 0b00001) > 0) {
                            next.add(x, y == 1 ? h - 2 : y - 1, 0b00001);
                        }
                        // >
                        if ((val & 0b00010) > 0) {
                            next.add(x == w - 2 ? 1 : x + 1, y, 0b00010);
                        }
                        // v
                        if ((val & 0b00100) > 0) {
                            next.add(x, y == h - 2 ? 1 : y + 1, 0b00100);
                        }
                        // <
                        if ((val & 0b01000) > 0) {
                            next.add(x == 1 ? w - 2 : x - 1, y, 0b01000);
                        }
                        // #
                        if (val == 0b10000) {
                            next.set(x, y, 0b10000);
                        }
                    }
                }
            }
            return next;
        }

        int findShortestDistance(Point2d start, Point2d end, int t) {
            Set<QueueEntry> visited = new HashSet<>();
            Queue<QueueEntry> q = new LinkedList<>();
            q.add(new QueueEntry(start, t));

            while (!q.isEmpty()) {
                QueueEntry e = q.poll();

                if (end.equals(e.p)) {
                    return e.t;
                }

                if (visited.contains(e)) continue;
                visited.add(e);

                Matrix2d m = getMapAtTime(e.t + 1);

                if (m.get(e.p) == 0) {
                    // we stay at the same position
                    q.add(new QueueEntry(e.p, e.t + 1));
                }

                for (Point2d d : Point2d.ALL_DIRS) {
                    Point2d newP = e.p.add(d);
                    if (m.isValidPosition(newP) && m.get(newP) == 0) q.add(new QueueEntry(newP, e.t + 1));
                }
            }

            return -1;
        }

        Matrix2d getMapAtTime(int t) {
            while (mapOverTime.size() - 1 < t) {
                Matrix2d lastMap = mapOverTime.get(mapOverTime.size() - 1);
                mapOverTime.add(simulateStep(lastMap));
            }

            return mapOverTime.get(t);
        }

        record QueueEntry(Point2d p, int t) {}
    }
}
