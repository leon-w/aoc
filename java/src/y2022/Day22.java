package y2022;


import utils.Matrix2d;
import utils.Point2d;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.function.Consumer;
import java.util.regex.MatchResult;
import java.util.regex.Pattern;
import java.util.stream.Stream;

public class Day22 {
    static final int AIR = 0;
    static final int ROCK = 1;
    static final int VOID = 2;


    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static Input readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/22.txt"))) {
            List<String> lines = stream.toList();

            String instructionsRaw = lines.get(lines.size() - 1);
            List<String> instructions = Pattern.compile("\\d+|[LR]")
                    .matcher(instructionsRaw)
                    .results()
                    .map(MatchResult::group)
                    .toList();

            List<String> mapLines = lines.subList(0, lines.size() - 2);
            int maxLen = mapLines.stream().mapToInt(String::length).max().orElseThrow();
            Matrix2d map = new Matrix2d(maxLen, mapLines.size());
            map.fill(VOID);

            for (int y = 0; y < mapLines.size(); y++) {
                String line = mapLines.get(y);
                for (int x = 0; x < line.length(); x++) {
                    map.set(x, y, switch (line.charAt(x)) {
                        case '.' -> AIR;
                        case '#' -> ROCK;
                        default -> VOID;
                    });
                }
            }

            return new Input(map, instructions);
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static void part1() {
        Input input = readInput();
        Matrix2d map = input.map;

        Point2d pos = null;
        for (int x = 0; x < map.w; x++) {
            if (map.get(x, 0) == AIR) {
                pos = new Point2d(x, 0);
                break;
            }
        }
        assert pos != null;

        int d = 0;
        Point2d[] dMap = new Point2d[]{Point2d.RIGHT, Point2d.DOWN, Point2d.LEFT, Point2d.UP};

        for (String ins : input.instructions) {
            if (ins.equals("L")) {
                d = (d - 1 + 4) % 4;
            } else if (ins.equals("R")) {
                d = (d + 1) % 4;
            } else {
                int steps = Integer.parseInt(ins);
                for (int i = 0; i < steps; i++) {
                    Point2d nextPos = pos.add(dMap[d]);
                    int tile = map.isValidPosition(nextPos) ? map.get(nextPos) : VOID;
                    if (tile == ROCK) break;
                    if (tile != AIR) {
                        Point2d otherDir = dMap[(d + 2) % 4];
                        Point2d wrapped = pos;
                        Point2d next = wrapped.add(otherDir);
                        while (map.isValidPosition(next) && map.get(next) != VOID) {
                            wrapped = next;
                            next = next.add(otherDir);
                        }
                        if (map.get(wrapped) == AIR) {
                            pos = wrapped;
                        } else {
                            break;
                        }
                    } else {
                        pos = nextPos;
                    }
                }
            }
        }

        int password = (pos.y + 1) * 1000 + (pos.x + 1) * 4 + d;

        System.out.println(password);
    }

    static void part2() {
        Input input = readInput();
        Matrix2d map = input.map;

        // cut map into blocks
        int block = Math.max(map.w, map.h) / 4;
        int blocksW = map.w / block;
        int blocksH = map.h / block;
        Face[][] faces = new Face[blocksH][blocksW];
        Point2d firstFacePos = null;
        int id = 0;
        for (int y = 0; y < blocksH; y++) {
            for (int x = 0; x < blocksW; x++) {
                Matrix2d sub = map.subMatrix(x * block, (x + 1) * block, y * block, (y + 1) * block);
                if (sub.count(VOID) != block * block) {
                    faces[y][x] = new Face(sub, id++);
                    if (firstFacePos == null) {
                        firstFacePos = new Point2d(x, y);
                    }
                }
            }
        }

        assert firstFacePos != null;

        // add tree links to faces
        Set<Point2d> visited = new HashSet<>();
        Queue<Point2d> q = new LinkedList<>();
        q.add(firstFacePos);

        while (!q.isEmpty()) {
            Point2d p = q.poll();

            if (visited.contains(p)) {
                continue;
            }
            visited.add(p);

            Face face = faces[p.y][p.x];

            for (int dir = 0; dir < 4; dir++) {
                Point2d newP = p.add(Point2d.ALL_DIRS[dir]);
                if (newP.x >= 0 && newP.x < blocksW && newP.y >= 0 && newP.y < blocksH) {
                    Face nextFace = faces[newP.y][newP.x];
                    if (nextFace != null && !visited.contains(newP)) {
                        face.sides[dir] = nextFace;
                        q.add(newP);
                    }
                }
            }
        }

        // fold and connect sides
        Face topFace = faces[firstFacePos.y][firstFacePos.x];
        topFace.fold();
        topFace.stitchSides();

        int d = 0;
        Point2d pos = new Point2d(0, 0);
        Point2d[] dMap = new Point2d[]{Point2d.RIGHT, Point2d.DOWN, Point2d.LEFT, Point2d.UP};

        for (String ins : input.instructions) {
            if (ins.equals("L")) {
                d = (d - 1 + 4) % 4;
            } else if (ins.equals("R")) {
                d = (d + 1) % 4;
            } else {
                for (int steps = Integer.parseInt(ins); steps > 0; steps--) {
                    Point2d nextPos = pos.add(dMap[d]);
                    int tile = topFace.surface.isValidPosition(nextPos) ? topFace.surface.get(nextPos) : VOID;
                    if (tile == ROCK) break;
                    if (tile != AIR) {
                        Face newTopFace = topFace.sides[(d + 1) % 4];
                        int incomingDir = 0;
                        for (; incomingDir < 4; incomingDir++) {
                            Face side = newTopFace.sides[incomingDir];
                            if (topFace == side) break;
                        }
                        int newD = (incomingDir + 1) % 4;
                        int validCoordinate = (d % 2 == 0) ? pos.y : pos.x;

                        // this checks if the connected sides are opposite, meaning that low values should be high values
                        if (((d == 0 || d == 3) && (newD == 1 || newD == 2)) || ((d == 1 || d == 2) && (newD == 0 || newD == 3))) {
                            validCoordinate = block - 1 - validCoordinate;
                        }

                        Point2d newPos = switch (newD) {
                            case 0 -> new Point2d(0, validCoordinate);
                            case 1 -> new Point2d(validCoordinate, 0);
                            case 2 -> new Point2d(block - 1, validCoordinate);
                            case 3 -> new Point2d(validCoordinate, block - 1);
                            default -> throw new IllegalStateException("Unexpected value: " + newD);
                        };

                        if (newTopFace.surface.get(newPos) == AIR) {
                            topFace = newTopFace;
                            d = newD;
                            pos = newPos;
                        } else {
                            break;
                        }
                    } else {
                        pos = nextPos;
                    }
                }
            }
        }

        // find initial positions and compute password
        for (int y = 0; y < blocksH; y++) {
            for (int x = 0; x < blocksW; x++) {
                Face f = faces[y][x];
                if (f != null && f == topFace) {
                    Point2d finalPos = new Point2d(block * x, block * y).add(pos);
                    int password = (finalPos.y + 1) * 1000 + (finalPos.x + 1) * 4 + d;

                    System.out.println(password);
                    return;
                }
            }
        }
    }


    record Input(Matrix2d map, List<String> instructions) {}

    static class Face {
        private static final int ZP = 0;
        private static final int YP = 1;
        private static final int XP = 2;
        private static final int YN = 3;
        private static final int XN = 4;
        private static final int ZN = 5;

        private static final int[][] NORMAL_MAP = {
                {YP, XP, YN, XN},
                {ZP, XN, ZN, XP},
                {ZP, YP, ZN, YN},
                {ZP, XP, ZN, XN},
                {ZP, YN, ZN, YP},
                {YN, XP, YP, XN},
        };

        private static final int[][] ROTATION_MAP = {
                {2, 3, 0, 1}, {2, 0, 2, 0}, {1, 0, 3, 0}, {0, 0, 0, 0}, {3, 0, 1, 0}, {0, 1, 2, 3},
        };

        Matrix2d surface;
        int id;
        Face[] sides = new Face[4];

        private int rotation = 0;
        private int normal = ZP;

        public Face(Matrix2d surface, int id) {
            this.surface = surface;
            this.id = id;
        }

        public void walk(Consumer<Face> consumer, Set<Integer> visited) {
            if (visited.contains(id)) return;
            visited.add(id);

            consumer.accept(this);
            for (int dir = 0; dir < 4; dir++) {
                Face n = getSide(dir);
                if (n != null) n.walk(consumer, visited);
            }
        }

        public Face getSide(int i) {
            return sides[(i + (4 - rotation)) % 4];
        }

        public void setSide(int i, Face side) {
            sides[(i + (4 - rotation)) % 4] = side;
        }

        public void fold() {
            for (int dir = 0; dir < 4; dir++) {
                Face n = getSide(dir);
                if (n != null) {
                    int finalDir = dir;
                    n.walk(f -> {
                        f.rotation = (f.rotation + (4 - ROTATION_MAP[normal][finalDir])) % 4;
                        f.normal = NORMAL_MAP[normal][finalDir];
                    }, new HashSet<>());
                    n.fold();
                }
            }
        }

        public void stitchSides() {
            Face[] cubeSides = new Face[6];
            walk(face -> cubeSides[face.normal] = face, new HashSet<>());

            walk(face -> {
                for (int dir = 0; dir < 4; dir++) {
                    face.setSide(dir, cubeSides[NORMAL_MAP[face.normal][dir]]);
                }
            }, new HashSet<>());
        }
    }
}
