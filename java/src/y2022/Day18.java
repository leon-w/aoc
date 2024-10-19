package y2022;


import utils.Point3d;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Day18 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static Set<Point3d> readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/18.txt"))) {
            return stream.map(s -> {
                String[] parts = s.split(",");
                return new Point3d(Integer.parseInt(parts[0]), Integer.parseInt(parts[1]), Integer.parseInt(parts[2]));
            }).collect(Collectors.toSet());
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static int countFaces(Set<Point3d> points) {
        int sideCount = 0;
        for (Point3d pos : points) {
            for (Point3d dir : Point3d.ALL_DIRS) {
                Point3d neighbor = pos.add(dir);
                if (!points.contains(neighbor)) sideCount++;
            }
        }
        return sideCount;
    }

    static void part1() {
        Set<Point3d> points = readInput();
        int faceCount = countFaces(points);
        System.out.println(faceCount);
    }

    static void part2() {
        Set<Point3d> points = readInput();

        int minX = Integer.MAX_VALUE;
        int maxX = Integer.MIN_VALUE;
        int minY = Integer.MAX_VALUE;
        int maxY = Integer.MIN_VALUE;
        int minZ = Integer.MAX_VALUE;
        int maxZ = Integer.MIN_VALUE;
        for (Point3d p : points) {
            minX = Math.min(minX, p.x);
            maxX = Math.max(maxX, p.x);
            minY = Math.min(minY, p.y);
            maxY = Math.max(maxY, p.y);
            minZ = Math.min(minZ, p.z);
            maxZ = Math.max(maxZ, p.z);
        }

        Set<Point3d> candidates = new HashSet<>();
        for (Point3d p : points) {
            for (Point3d d : Point3d.ALL_DIRS) {
                Point3d newP = p.add(d);
                if (!points.contains(newP)) {
                    candidates.add(newP);
                }
            }
        }

        Set<Point3d> confirmedInside = new HashSet<>();
        Set<Point3d> confirmedOutside = new HashSet<>();
        for (Point3d candidate : candidates) {
            if (confirmedInside.contains(candidate) || confirmedOutside.contains(candidate)) continue;

            Set<Point3d> visited = new HashSet<>();
            Queue<Point3d> q = new LinkedList<>();
            q.add(candidate);
            boolean isOutside = false;
            while (!q.isEmpty()) {
                Point3d p = q.poll();

                if (visited.contains(p) || points.contains(p)) continue;
                visited.add(p);

                if (confirmedInside.contains(p)) {
                    break;
                }

                if (confirmedOutside.contains(p)) {
                    isOutside = true;
                    break;
                }

                if (p.x <= minX || p.x >= maxX || p.y <= minY || p.y >= maxY || p.z <= minZ || p.z >= maxZ) {
                    isOutside = true;
                    break;
                }

                for (Point3d d : Point3d.ALL_DIRS) {
                    q.add(p.add(d));
                }
            }

            if (isOutside) {
                confirmedOutside.addAll(visited);
            } else {
                confirmedInside.addAll(visited);
            }
        }

        points.addAll(confirmedInside);
        int faceCount = countFaces(points);
        System.out.println(faceCount);
    }
}
