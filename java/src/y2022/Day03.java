package y2022;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Day03 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static List<String> readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/03.txt"))) {
            return stream.toList();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static Set<Integer> toSet(String s) {
        return s.chars().boxed().collect(Collectors.toSet());
    }

    static void part1() {
        var input = readInput();
        int pSum = 0;
        for (String line : input) {
            int halfLen = line.length() / 2;
            var lSet = toSet(line.substring(0, halfLen));
            var rSet = toSet(line.substring(halfLen));

            for (int c : lSet) {
                if (rSet.contains(c)) {
                    pSum += c <= 'Z' ? c - 'A' + 27 : c - 'a' + 1;
                    break;
                }
            }
        }
        System.out.println(pSum);
    }

    static void part2() {
        var input = readInput();
        int pSum = 0;
        for (int i = 0; i < input.size(); i += 3) {
            var set1 = toSet(input.get(i));
            var set2 = toSet(input.get(i + 1));
            var set3 = toSet(input.get(i + 2));

            for (int c : set1) {
                if (set2.contains(c) && set3.contains(c)) {
                    pSum += c <= 'Z' ? c - 'A' + 27 : c - 'a' + 1;
                    break;
                }
            }
        }
        System.out.println(pSum);
    }
}
