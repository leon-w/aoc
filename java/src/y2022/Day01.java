package y2022;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Stream;

public class Day01 {
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
        try (Stream<String> stream = Files.lines(Paths.get("inputs/01.txt"))) {
            return stream.toList();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static void part1() {
        var input = readInput();
        int maxElf = 0;
        int acc = 0;
        for (String line : input) {
            if (line.length() == 0) {
                maxElf = Math.max(maxElf, acc);
                acc = 0;
            } else {
                acc += Integer.parseInt(line);
            }
        }
        System.out.println(maxElf);
    }

    static void part2() {
        var input = readInput();
        List<Integer> elfs = new ArrayList<>();
        int acc = 0;
        for (String line : input) {
            if (line.length() == 0) {
                elfs.add(acc);
                acc = 0;
            } else {
                acc += Integer.parseInt(line);
            }
        }

        elfs.sort(Comparator.reverseOrder());

        System.out.println(elfs.get(0) + elfs.get(1) + elfs.get(2));
    }
}
