package y2022;


import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

public class Day13 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static List<JsonElement> readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/13.txt"))) {
            return stream.filter(s -> !s.isEmpty()).map(JsonParser::parseString).toList();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static int compare(JsonElement left, JsonElement right) {
        if (left.isJsonPrimitive() && right.isJsonPrimitive()) {
            int leftNum = left.getAsInt();
            int rightNum = right.getAsInt();
            return Integer.compare(leftNum, rightNum);
        }

        if (left.isJsonArray() && right.isJsonArray()) {
            JsonArray leftArr = left.getAsJsonArray();
            JsonArray rightArr = right.getAsJsonArray();

            int minLen = Math.min(leftArr.size(), rightArr.size());
            for (int i = 0; i < minLen; i++) {
                int comp = compare(leftArr.get(i), rightArr.get(i));
                if (comp != 0) return comp;
            }
            return Integer.compare(leftArr.size(), rightArr.size());
        }

        if (left.isJsonArray()) {
            JsonArray rightArr = new JsonArray();
            rightArr.add(right);
            return compare(left, rightArr);
        }

        if (right.isJsonArray()) {
            JsonArray leftArr = new JsonArray();
            leftArr.add(left);
            return compare(leftArr, right);
        }

        return 0;
    }

    static void part1() {
        List<JsonElement> input = readInput();

        int sum = 0;
        for (int i = 0; i < input.size(); i += 2) {
            JsonElement left = input.get(i);
            JsonElement right = input.get(i + 1);
            if (compare(left, right) == -1) {
                sum += i / 2 + 1;
            }
        }
        System.out.println(sum);
    }

    static void part2() {
        // make input mutable
        List<JsonElement> input = new ArrayList<>(readInput());

        JsonElement divider1 = JsonParser.parseString("[[2]]");
        JsonElement divider2 = JsonParser.parseString("[[6]]");

        input.add(divider1);
        input.add(divider2);

        input.sort(Day13::compare);

        int index1 = input.indexOf(divider1) + 1;
        int index2 = input.indexOf(divider2) + 1;
        int prod = index1 * index2;

        System.out.println(prod);
    }
}
