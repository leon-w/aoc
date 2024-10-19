package y2022;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

public class Day17 {
    final static boolean T = true;
    final static boolean F = false;
    final static Rock[] rocks = new Rock[]{
            new Rock(new boolean[][]{{T, T, T, T}}, 0),
            new Rock(new boolean[][]{{F, T, F}, {T, T, T}, {F, T, F}}, 1),
            new Rock(new boolean[][]{{F, F, T}, {F, F, T}, {T, T, T}}, 2),
            new Rock(new boolean[][]{{T}, {T}, {T}, {T}}, 3),
            new Rock(new boolean[][]{{T, T}, {T, T}}, 4),
    };

    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static char[] readInput() {
        try {
            return Files.readString(Paths.get("inputs/17.txt")).toCharArray();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static void part1() {
        char[] streams = readInput();

        Tower tower = new Tower(streams);

        for (int loop = 0; loop < 2022; loop++) tower.simulateRock();

        System.out.println(tower.getHeight());
    }

    static void part2() {
        char[] streams = readInput();

        Tower tower = new Tower(streams);

        Set<Integer> knownStates = new HashSet<>();

        boolean dupeFound = false;
        int firstDupeHash = 0;
        long firstDupeRockCount = 0;
        long firstDupeHeight = 0;

        long loopRockCount;
        long loopHeight;

        for (int i = 0; ; i++) {
            int stateHash = Objects.hash(tower.getHashOfStackTop(16), tower.t, tower.r);
            if (dupeFound) {
                if (stateHash == firstDupeHash) {
                    loopRockCount = i - firstDupeRockCount;
                    loopHeight = tower.getHeight() - firstDupeHeight;
                    break;
                }
            } else {
                if (knownStates.contains(stateHash)) {
                    dupeFound = true;
                    firstDupeHash = stateHash;
                    firstDupeRockCount = i;
                    firstDupeHeight = tower.getHeight();
                } else {
                    knownStates.add(stateHash);
                }
            }
            tower.simulateRock();
        }

        long targetRockCount = 1000000000000L;

        long cycles = (targetRockCount - firstDupeRockCount) / loopRockCount;
        long extra = (targetRockCount - firstDupeRockCount) % loopRockCount;

        long heightBefore = tower.getHeight();
        for (int i = 0; i < extra; i++) tower.simulateRock();
        long addedHeight = tower.getHeight() - heightBefore;

        long finalHeight = firstDupeHeight + cycles * loopHeight + addedHeight;

        System.out.println(finalHeight);
    }

    static class Tower {
        private static final int AIR = 0;
        private static final int ROCK = 1;
        private final List<Stack<Integer>> stacks;
        private final char[] streams;
        int t = 0;
        int r = 0;

        Tower(char[] streams) {
            stacks = new ArrayList<>(7);
            for (int i = 0; i < 7; i++) {
                stacks.add(new Stack<>());
            }
            this.streams = streams;
        }

        void simulateRock() {
            Rock rock = rocks[r];
            r = (r + 1) % rocks.length;

            int rockX = 2;
            int rockY = getHeight() + 3;

            while (true) {
                // move sideways
                char stream = streams[t];
                t = (t + 1) % streams.length;

                if (stream == '>') {
                    if (isValidPosForRock(rockX + 1, rockY, rock)) {
                        rockX++;
                    }
                } else {
                    if (isValidPosForRock(rockX - 1, rockY, rock)) {
                        rockX--;
                    }
                }

                // move down
                if (isValidPosForRock(rockX, rockY - 1, rock)) {
                    rockY--;
                } else {
                    placeRock(rockX, rockY, rock);
                    break;
                }
            }
        }

        int getHeight() {
            return stacks.stream().mapToInt(Stack::size).max().orElseThrow();
        }

        private int getBlock(int x, int y) {
            Stack<Integer> s = stacks.get(x);
            if (s.size() > y) return s.get(y);
            return AIR;
        }

        private void setBlock(int x, int y, int block) {
            Stack<Integer> s = stacks.get(x);
            if (s.size() > y) {
                s.set(y, block);
            } else {
                while (s.size() < y) s.push(AIR);
                s.push(block);
            }
        }

        private boolean isValidPosForRock(int rockX, int rockY, Rock rock) {
            if (rockX < 0 || rockX + rock.w > 7 || rockY < 0) return false;

            for (int x = 0; x < rock.w; x++) {
                for (int y = 0; y < rock.h; y++) {
                    if (rock.isSolidAt(x, y) && getBlock(rockX + x, rockY + y) != AIR) {
                        return false;
                    }
                }
            }

            return true;
        }

        private void placeRock(int rockX, int rockY, Rock rock) {
            for (int x = 0; x < rock.w; x++) {
                for (int y = 0; y < rock.h; y++) {
                    if (rock.isSolidAt(x, y)) setBlock(rockX + x, rockY + y, ROCK + rock.id + 1);
                }
            }
        }

        int getHashOfStackTop(int h) {
            int maxH = getHeight();

            int result = 1;
            for (int y = 0; y < Math.min(h, maxH); y++) {
                int row = 0;
                for (int x = 0; x < 7; x++) {
                    row <<= 1;
                    row += getBlock(x, maxH - y - 1) == AIR ? 0 : 1;
                }
                // hash based on Arrays.hash
                result = 31 * result + row;
            }

            return result;
        }

        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();

            for (int y = getHeight() - 1; y >= 0; y--) {
                sb.append('|');
                for (int x = 0; x < 7; x++) {
                    sb.append(switch (getBlock(x, y)) {
                        case AIR -> '.';
                        case ROCK -> '#';
                        case ROCK + 1 -> "\u001B[31m#\u001B[0m";
                        case ROCK + 2 -> "\u001B[36m#\u001B[0m";
                        case ROCK + 3 -> "\u001B[33m#\u001B[0m";
                        case ROCK + 4 -> "\u001B[34m#\u001B[0m";
                        case ROCK + 5 -> "\u001B[35m#\u001B[0m";
                        default -> '?';
                    });
                }
                sb.append("|\n");
            }
            sb.append("+-------+");

            return sb.toString();
        }
    }

    static class Rock {
        final int w;
        final int h;
        final int id;
        private final boolean[][] shape;

        Rock(boolean[][] shape, int id) {
            this.shape = shape;
            this.id = id;

            w = shape[0].length;
            h = shape.length;
        }

        boolean isSolidAt(int x, int y) {
            return shape[h - y - 1][x];
        }
    }
}
