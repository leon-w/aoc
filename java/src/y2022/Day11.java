package y2022;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Day11 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static List<Monkey> readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/11.txt"))) {
            List<Monkey> monkeys = new ArrayList<>();
            String[] monkeyRaw = new String[6];
            int i = 0;
            for (String line : stream.toList()) {
                if (line.isEmpty()) {
                    continue;
                }

                monkeyRaw[i] = line;
                i++;
                if (i == 6) {
                    monkeys.add(new Monkey(monkeyRaw));
                    i = 0;
                }
            }
            return monkeys;
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static long computeMonkeyBusiness(List<Monkey> monkeys, int turns, boolean divideByThree) {
        long prod = monkeys.stream().mapToLong(m -> m.test).reduce(1, (a, b) -> a * b);

        for (int turn = 0; turn < turns; turn++) {
            for (Monkey monkey : monkeys) {
                while (!monkey.items.isEmpty()) {
                    long item = monkey.inspect(monkey.items.remove(0));
                    if (divideByThree) {
                        item /= 3;
                    }
                    item %= prod;
                    monkeys.get(item % monkey.test == 0 ? monkey.forwardTrue : monkey.forwardFalse).items.add(item);
                    monkey.inspected++;
                }
            }
        }

        return monkeys.stream()
                .sorted((m1, m2) -> m2.inspected - m1.inspected)
                .limit(2)
                .mapToLong(m -> m.inspected)
                .reduce(1, (a, b) -> a * b);
    }

    static void part1() {
        List<Monkey> monkeys = readInput();

        System.out.println(computeMonkeyBusiness(monkeys, 20, true));
    }

    static void part2() {
        List<Monkey> monkeys = readInput();

        System.out.println(computeMonkeyBusiness(monkeys, 10000, false));
    }

    static class Monkey {
        public int inspected = 0;

        List<Long> items;
        boolean opIsAdd;
        boolean opValIsOld;
        int opVal;
        int test;
        int forwardTrue;
        int forwardFalse;

        public Monkey(String[] lines) {
            // starting items
            String[] parts = lines[1].split(": ");
            if (parts.length > 1) {
                items = Arrays.stream(parts[1].split(", ")).map(Long::parseLong).collect(Collectors.toList());
            } else {
                items = new ArrayList<>();
            }

            // operation
            parts = lines[2].split(" ");
            opIsAdd = parts[parts.length - 2].equals("+");
            opValIsOld = parts[parts.length - 1].equals("old");
            if (!opValIsOld) {
                opVal = Integer.parseInt(parts[parts.length - 1]);
            }

            // test
            parts = lines[3].split(" ");
            test = Integer.parseInt(parts[parts.length - 1]);

            // test true
            parts = lines[4].split(" ");
            forwardTrue = Integer.parseInt(parts[parts.length - 1]);

            // test false
            parts = lines[5].split(" ");
            forwardFalse = Integer.parseInt(parts[parts.length - 1]);
        }

        public long inspect(long item) {
            long v = opValIsOld ? item : opVal;
            item = opIsAdd ? item + v : item * v;
            return item;
        }
    }
}
