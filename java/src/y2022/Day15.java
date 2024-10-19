package y2022;


import utils.Point2d;
import utils.Range;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

public class Day15 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static List<SensorBeaconPair> readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/15.txt"))) {
            Pattern pattern = Pattern.compile("Sensor at x=(-?\\d+), y=(-?\\d+): closest beacon is at x=(-?\\d+), y=(-?\\d+)");
            return stream.map(pattern::matcher).filter(Matcher::matches).map(m -> {
                Point2d sensor = new Point2d(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2)));
                Point2d beacon = new Point2d(Integer.parseInt(m.group(3)), Integer.parseInt(m.group(4)));
                return new SensorBeaconPair(sensor, beacon);
            }).toList();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static void part1() {
        List<SensorBeaconPair> input = readInput();

        List<Range> coveredRanges = new ArrayList<>();

        int targetY = 2000000;
        for (SensorBeaconPair pair : input) {
            int distance = pair.sensor.manhattanDistance(pair.beacon);
            int distY = Math.abs(targetY - pair.sensor.y);

            if (distY <= distance) {
                int remaining = distance - distY;
                int leftX = pair.sensor.x - remaining;
                int rightX = pair.sensor.x + remaining;
                coveredRanges.add(new Range(leftX, rightX + 1));
            }
        }

        coveredRanges.sort(Comparator.comparingInt(r -> r.start));

        int coveredCount = 0;
        if (!coveredRanges.isEmpty()) {
            int lastEnd = coveredRanges.get(0).start;
            for (Range r : coveredRanges) {
                if (r.end <= lastEnd) {
                    continue;
                }

                if (r.start >= lastEnd) {
                    // no overlap
                    coveredCount += r.size();
                } else {
                    // partial overlap
                    coveredCount += r.size() - (lastEnd - r.start - 1);
                }

                lastEnd = r.end;
            }
        }

        System.out.println(coveredCount);
    }

    static void part2() {
        List<SensorBeaconPair> input = readInput();

        StringBuilder mz = new StringBuilder();

        mz.append("var 0..4000000: x;\n");
        mz.append("var 0..4000000: y;\n");

        for (SensorBeaconPair pair : input) {
            int distance = pair.sensor.manhattanDistance(pair.beacon);
            mz.append(String.format("constraint abs(x - %d) + abs(y - %d) > %d;\n", pair.sensor.x, pair.sensor.y, distance));
        }

        System.out.println(mz);

        // we use MiniZinc to solve the constraint problem
        // HiGHS 1.6.0 finds a solution in around 250ms
        // Result:
        long x = 2936793;
        long y = 3442119;
        long tuningFrequency = x * 4000000 + y;

        System.out.println(tuningFrequency);
    }

    record SensorBeaconPair(Point2d sensor, Point2d beacon) {}
}
