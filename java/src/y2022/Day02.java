package y2022;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Stream;

public class Day02 {
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
        try (Stream<String> stream = Files.lines(Paths.get("inputs/02.txt"))) {
            return stream.toList();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static void part1() {
        var input = readInput();
        int score = 0;
        for (String line : input) {
            int o = line.charAt(0) - 'A';
            int m = line.charAt(2) - 'X';

            score += m + 1;
            if (m == o) {
                score += 3;
            } else if (m == (o + 1) % 3) {
                score += 6;
            }
        }
        System.out.println(score);
    }

    static void part2() {
        var input = readInput();
        int score = 0;
        for (String line : input) {
            int o = line.charAt(0) - 'A';
            int m = line.charAt(2) - 'X';

            if (m == 0) {
                m = (o - 1 + 3) % 3; // +3 to ensure positive result
            } else if (m == 1) {
                m = o;
            } else {
                m = (o + 1) % 3;
            }

            score += m + 1;
            if (m == o) {
                score += 3;
            } else if (m == (o + 1) % 3) {
                score += 6;
            }
        }
        System.out.println(score);
    }
}
