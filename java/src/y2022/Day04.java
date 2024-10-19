package y2022;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Stream;


public class Day04 {
    private record Pair<T>(T a, T b) {}

    private record Range(int start, int end) {
        public boolean contains(Range other) {
            return this.start <= other.start && this.end >= other.end;
        }

        public boolean overlaps(Range other) {
            Range smaller = this.start < other.start? this : other;
            Range bigger = this.start < other.start? other : this;
            return bigger.start <= smaller.end;
        }
    }

    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static List<Pair<Range>> readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/04.txt"))) {
            return stream.map(s -> {
                var ranges = Arrays.stream(s.split(",")).map(p -> {
                    String[] parts = p.split("-");
                    return new Range(Integer.parseInt(parts[0]), Integer.parseInt(parts[1]));
                }).toList();
                return new Pair<>(ranges.get(0), ranges.get(1));
            }).toList();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static void part1() {
        var pairs = readInput();
        long count = pairs.stream().filter(p -> p.a().contains(p.b()) || p.b().contains(p.a())).count();
        System.out.println(count);
    }

    static void part2() {
        var pairs = readInput();
        long count = pairs.stream().filter(p -> p.a().overlaps(p.b())).count();
        System.out.println(count);
    }
}
