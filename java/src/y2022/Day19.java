package y2022;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.regex.Pattern;
import java.util.stream.Stream;

public class Day19 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static List<Blueprint> readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/19.txt"))) {
            return stream.map(s -> {
                Pattern p = Pattern.compile("\\d+");
                int[] ns = p.matcher(s).results().mapToInt(r -> Integer.parseInt(r.group())).toArray();
                return new Blueprint(ns[1], ns[2], ns[3], ns[4], ns[5], ns[6]);
            }).toList();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static void part1() {
        List<Blueprint> blueprints = readInput();

        Optimizer opt = new Optimizer();

        long score = 0;
        for (int i = 0; i < blueprints.size(); i++) {
            opt.updateBlueprint(blueprints.get(i));

            long startMs = System.currentTimeMillis();
            long geodes = opt.opt(Optimizer.pack(new long[]{0, 0, 0, 0}), Optimizer.pack(new long[]{1, 0, 0, 0}), 24);
            long totalMs = System.currentTimeMillis() - startMs;

            System.out.printf("%d nodes generated, %d cache hits in %dms -> %d\n",
                    opt.nodesGenerated,
                    opt.cacheHits,
                    totalMs,
                    geodes);

            score += (i + 1) * geodes;
        }

        System.out.println(score);
    }

    static void part2() {
        List<Blueprint> blueprints = readInput();

        Optimizer opt = new Optimizer();

        long prod = 1;
        for (int i = 0; i < 3; i++) {
            opt.updateBlueprint(blueprints.get(i));

            long startMs = System.currentTimeMillis();
            long geodes = opt.opt(Optimizer.pack(new long[]{0, 0, 0, 0}), Optimizer.pack(new long[]{1, 0, 0, 0}), 32);
            long totalMs = System.currentTimeMillis() - startMs;

            System.out.printf("%d nodes generated, %d cache hits in %dms -> %d\n",
                    opt.nodesGenerated,
                    opt.cacheHits,
                    totalMs,
                    geodes);

            prod *= geodes;
        }

        System.out.println(prod);
    }

    static class Blueprint {
        final long[] recipes;

        Blueprint(int oreRobotOreCost, int clayRobotOreCost, int obsidianRobotOreCost, int obsidianRobotClayCost, int geodeRobotOreCost, int geodeRobotObsidianCost) {
            recipes = new long[]{
                    Optimizer.pack(new long[]{oreRobotOreCost, 0, 0, 0}),
                    Optimizer.pack(new long[]{clayRobotOreCost, 0, 0, 0}),
                    Optimizer.pack(new long[]{obsidianRobotOreCost, obsidianRobotClayCost, 0, 0}),
                    Optimizer.pack(new long[]{geodeRobotOreCost, 0, geodeRobotObsidianCost, 0}),
            };
        }
    }


    static class Optimizer {
        Blueprint bp = null;
        int nodesGenerated = 0;
        int cacheHits = 0;

        byte[] cache = new byte[2147462143];

        static long pack(long[] parts) {
            return (parts[0] << 48) | (parts[1] << 32) | (parts[2] << 16) | parts[3];
        }

        static long getPart(long l, int i) {
            return (l >>> (16 * (3 - i))) & 0xFFFFL;
        }

        public void updateBlueprint(Blueprint bp) {
            // to avoid reallocation of the cache
            this.bp = bp;
            Arrays.fill(cache, (byte) 255);
        }

        long opt(long mat, long rob, long t) {
            if (t == 0) return mat & 0xFFFFL;

            int hash = Objects.hash(mat, rob) % cache.length;
            if (hash < 0) hash += cache.length;
            byte hashVal = cache[hash];
            if (hashVal != (byte) 255 && hashVal >= t) {
                cacheHits++;
                // we already explored this path so and the maximum is already updated accordingly
                // so we can just return the dummy value 0
                return 0;
            }

            nodesGenerated++;

            long bestScore = (mat + rob * t) & 0xFFFFL;

            mat_loop:
            for (int robotCandidate = 0; robotCandidate < 4; robotCandidate++) {
                long cost = bp.recipes[robotCandidate];

                long steps = 0;
                for (int m = 0; m < 4; m++) {
                    long have = getPart(mat, m);
                    long need = getPart(cost, m);
                    if (have < need) {
                        long robForM = getPart(rob, m);
                        if (robForM == 0) continue mat_loop;
                        long stepsForM = (need - have + robForM - 1) / robForM;
                        if (stepsForM >= t) continue mat_loop;
                        steps = Math.max(steps, stepsForM);
                    }
                }

                long tNew = t - steps - 1;
                long matNew = mat + (steps + 1) * rob - cost;
                long robNew = rob + (1L << ((3 - robotCandidate) * 16));

                bestScore = Math.max(bestScore, opt(matNew, robNew, tNew));
            }

            cache[hash] = (byte) t;

            return bestScore;
        }
    }
}
