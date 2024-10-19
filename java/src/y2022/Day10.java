package y2022;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Stream;


public class Day10 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static List<Instruction> readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/10.txt"))) {
            return stream.map(s -> {
                if (s.equals("noop")) {
                    return new Instruction(true, 0);
                }
                String[] parts = s.split(" ");
                return new Instruction(false, Integer.parseInt(parts[1]));
            }).toList();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }


    static void part1() {
        List<Instruction> instructions = readInput();

        int x = 1;

        int pc = 0;
        int clock = 0;
        boolean addPending = false;
        int pendingValue = 0;

        int signalSum = 0;
        while (clock <= 220) {
            clock++;

            if ((clock - 20) % 40 == 0) {
                signalSum += clock * x;
            }

            if (addPending) {
                x += pendingValue;
                addPending = false;
            } else {
                if (pc >= instructions.size()) {
                    break;
                }
                Instruction ins = instructions.get(pc);
                pc++;
                if (!ins.isNoop) {
                    addPending = true;
                    pendingValue = ins.value;
                }
            }
        }

        System.out.println(signalSum);
    }

    static void part2() {
        List<Instruction> instructions = readInput();

        int x = 1;

        int pc = 0;
        int clock = 0;
        boolean addPending = false;
        int pendingValue = 0;

        char[] screen = new char[240];

        while (clock < 240) {
            screen[clock] = Math.abs(x - (clock % 40)) <= 1 ? '#' : '.';

            clock++;

            if (addPending) {
                x += pendingValue;
                addPending = false;
            } else {
                if (pc >= instructions.size()) {
                    break;
                }
                Instruction ins = instructions.get(pc);
                pc++;
                if (!ins.isNoop) {
                    addPending = true;
                    pendingValue = ins.value;
                }
            }
        }

        for (int i = 0; i < 240; i++) {
            System.out.print(screen[i]);
            if (i % 40 == 39) {
                System.out.println();
            }
        }
    }

    record Instruction(boolean isNoop, int value) {}
}
