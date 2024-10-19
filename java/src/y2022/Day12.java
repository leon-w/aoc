package y2022;


import utils.Matrix2d;
import utils.Point2d;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Set;
import java.util.stream.Stream;

public class Day12 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static Input readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/12.txt"))) {
            var rows = stream.map(s -> s.chars().toArray()).toList();
            var matrix = new Matrix2d(rows.toArray(new int[rows.size()][rows.get(0).length]));

            Point2d start = null;
            Point2d end = null;
            for (Point2d p : matrix.iterateCoords()) {
                if (matrix.get(p) == 'S') {
                    start = p;
                    matrix.set(p, 'a');
                    if (end != null) break;
                } else if (matrix.get(p) == 'E') {
                    end = p;
                    matrix.set(p, 'z');
                    if (start != null) break;
                }
            }
            return new Input(matrix, start, end);
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static void part1() {
        Input input = readInput();

        Matrix2d map = input.map;
        Point2d start = input.start;
        Point2d end = input.end;

        Set<Point2d> visited = new HashSet<>();
        Queue<QueueEntry> q = new LinkedList<>();

        q.add(new QueueEntry(start, 0));

        while (!q.isEmpty()) {
            QueueEntry e = q.poll();

            if (visited.contains(e.p)) continue;
            visited.add(e.p);

            if (e.p.equals(end)) {
                System.out.println(e.d);
                break;
            }

            int currentH = map.get(e.p);
            for (Point2d dir : Point2d.ALL_DIRS) {
                Point2d newP = e.p.copy().addI(dir);
                if (map.isValidPosition(newP) && map.get(newP) <= currentH + 1) {
                    q.add(new QueueEntry(newP, e.d + 1));
                }
            }
        }
    }

    static void part2() {
        Input input = readInput();

        Matrix2d map = input.map;
        Point2d end = input.end;

        int shortestDist = Integer.MAX_VALUE;

        Set<Point2d> visited = new HashSet<>();
        Queue<QueueEntry> q = new LinkedList<>();

        q.add(new QueueEntry(end, 0));

        while (!q.isEmpty()) {
            QueueEntry e = q.poll();

            if (visited.contains(e.p)) continue;
            visited.add(e.p);

            if (map.get(e.p) == 'a') {
                shortestDist = Math.min(shortestDist, e.d);
            }

            int currentH = map.get(e.p);
            for (Point2d dir : Point2d.ALL_DIRS) {
                Point2d newP = e.p.copy().addI(dir);
                if (map.isValidPosition(newP) && map.get(newP) + 1 >= currentH) {
                    q.add(new QueueEntry(newP, e.d + 1));
                }
            }
        }

        System.out.println(shortestDist);
    }

    record Input(Matrix2d map, Point2d start, Point2d end) {}

    record QueueEntry(Point2d p, int d) {}
}
