package y2022;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.LinkedList;
import java.util.List;
import java.util.stream.Stream;

public class Day20 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static int[] readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/20.txt"))) {
            return stream.mapToInt(Integer::parseInt).toArray();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static void part1() {
        int[] values = readInput();

        CircularList l = new CircularList();
        for (int val : values) l.add(val);

        l.mix();

        System.out.println(l.computeAnswer());
    }

    static void part2() {
        int[] values = readInput();

        CircularList l = new CircularList();
        for (int val : values) l.add(val * 811589153L);

        // mix 10 times
        for (int i = 0; i < 10; i++) l.mix();

        System.out.println(l.computeAnswer());
    }

    static class CircularList {
        Node entry = null;
        int len = 0;

        void add(long val) {
            Node n = new Node(val, len);
            len++;
            if (entry == null) {
                n.next = n;
                n.prev = n;
                entry = n;
                return;
            }
            Node prevBefore = entry.prev;
            entry.prev = n;
            n.next = entry;
            n.prev = prevBefore;
            prevBefore.next = n;
        }

        void mix() {
            if (len < 2) return;

            for (int initialIndex = 0; initialIndex < len; initialIndex++) {
                // find relevant node
                Node n = entry;
                while (n.insertIndex != initialIndex) {
                    n = n.next;
                }

                // remove node
                n.prev.next = n.next;
                n.next.prev = n.prev;
                if (entry == n) {
                    entry = n.next;
                }

                // move to target
                Node current = n.next;
                long move = n.val % (len - 1);
                if (move > 0) {
                    for (int i = 0; i < move; i++) {
                        current = current.next;
                    }
                } else {
                    for (int i = 0; i < -move; i++) {
                        current = current.prev;
                    }
                }

                // insert back
                Node prevBefore = current.prev;
                current.prev = n;
                n.next = current;
                n.prev = prevBefore;
                prevBefore.next = n;
            }
        }

        long computeAnswer() {
            // find 0
            Node n = entry;
            while (n.val != 0) {
                n = n.next;
            }

            long answer = 0;
            for (int i = 0; i < 3; i++) {
                // move forward 1000 steps
                int move = 1000 % len;
                while (move > 0) {
                    n = n.next;
                    move--;
                }
                answer += n.val;
            }

            return answer;
        }

        List<Long> toList() {
            List<Long> l = new LinkedList<>();
            if (entry != null) {
                Node current = entry;
                do {
                    l.add(current.val);
                    current = current.next;
                } while (current != entry);
            }
            return l;
        }

        private static class Node {
            long val;
            int insertIndex;
            Node next = null;
            Node prev = null;

            Node(long val, int insertIndex) {
                this.val = val;
                this.insertIndex = insertIndex;
            }
        }
    }
}
