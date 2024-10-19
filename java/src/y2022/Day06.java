package y2022;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Day06 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static String readInput() {
        try {
            return Files.readString(Paths.get("inputs/06.txt"));
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static int findUniqueSequence(String s, int len) {
        for (int i = len - 1; i < s.length(); i++) {
            if (s.substring(i - len + 1, i + 1).chars().distinct().count() == len) {
                return i + 1;
            }
        }
        return -1;
    }

    static void part1() {
        var data = readInput();
        System.out.println(findUniqueSequence(data, 4));
    }

    static void part2() {
        var data = readInput();
        System.out.println(findUniqueSequence(data, 14));
    }
}
