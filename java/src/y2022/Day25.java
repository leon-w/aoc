package y2022;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Stream;

public class Day25 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
    }

    static List<String> readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/25.txt"))) {
            return stream.toList();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static long snafuToDec(String s) {
        long n = 0;
        long p = 1;
        for (int i = s.length() - 1; i >= 0; i--) {
            n += p * switch (s.charAt(i)) {
                case '=' -> -2;
                case '-' -> -1;
                case '1' -> 1;
                case '2' -> 2;
                default -> 0;
            };
            p *= 5;
        }
        return n;
    }

    static String decToSnafu(long n) {
        StringBuilder sb = new StringBuilder();

        long carry = 0;
        while (n > 0 || carry > 0) {
            long rem = n % 5;
            n /= 5;

            rem += carry;
            carry = rem / 5;

            rem %= 5;

            if (rem >= 3) carry++;

            if (rem == 3) {
                sb.append('=');
            } else if (rem == 4) {
                sb.append('-');
            } else {
                sb.append(rem);
            }

        }

        return sb.reverse().toString();
    }

    static void part1() {
        List<String> input = readInput();

        long sum = input.stream().mapToLong(Day25::snafuToDec).sum();
        String sumSnafu = decToSnafu(sum);

        System.out.println(sumSnafu);
    }
}
