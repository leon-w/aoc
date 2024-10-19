package y2022;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Stack;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;


public class Day05 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    private static List<Stack<Character>> parseStacks(List<String> lines) {
        List<Stack<Character>> stacks = new ArrayList<>();
        int totalStacks = lines.get(lines.size() - 1).length() / 4 + 1;
        for (int i = 0; i < totalStacks; i++) {
            stacks.add(new Stack<>());
        }

        for (String line : lines) {
            for (int i = 0; i < line.length(); i++) {
                char c = line.charAt(i);
                if (c >= 'A' && c <= 'Z') {
                    int idx = i / 4;
                    stacks.get(idx).add(0, c);
                }
            }
        }

        return stacks;
    }

    static Input readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/05.txt"))) {
            var lines = stream.toList();
            var sepIndex = lines.indexOf("");
            var stacks = parseStacks(lines.subList(0, sepIndex));

            Pattern movePattern = Pattern.compile("move (\\d+) from (\\d+) to (\\d+)");
            var moves =
                    lines.subList(sepIndex + 1, lines.size())
                            .stream()
                            .map(movePattern::matcher)
                            .filter(Matcher::matches)
                            .map(m -> new Move(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2)), Integer.parseInt(m.group(3))))
                            .toList();

            return new Input(stacks, moves);
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static String processStacks(Input input, boolean keepOrder) {
        var stacks = input.stacks;
        var moves = input.moves;

        for (Move m : moves) {
            var source = stacks.get(m.from - 1);
            var target = stacks.get(m.to - 1);
            int insertIndex = target.size();
            for (int i = 0; i < m.amount; i++) {
                if (keepOrder) {
                    target.add(insertIndex, source.pop());
                } else {
                    target.push(source.pop());
                }
            }
        }

        return stacks.stream().map(Stack::peek).map(String::valueOf).collect(Collectors.joining());
    }

    static void part1() {
        Input input = readInput();

        System.out.println(processStacks(input, false));
    }

    static void part2() {
        Input input = readInput();

        System.out.println(processStacks(input, true));
    }

    record Move(int amount, int from, int to) {}

    record Input(List<Stack<Character>> stacks, List<Move> moves) {}
}
