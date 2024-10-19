package y2022;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Consumer;
import java.util.stream.Stream;

public class Day07 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static Directory readInput() {
        Directory cwd = new Directory("/", null);
        try (Stream<String> stream = Files.lines(Paths.get("inputs/07.txt"))) {
            boolean inLs = false;

            for (String s : stream.toList()) {
                if (s.startsWith("$")) {
                    if (s.contains("cd")) {
                        inLs = false;
                        String[] parts = s.split(" ");
                        String path = parts[parts.length - 1];
                        if (!path.equals("/")) {
                            cwd = cwd.cd(path);
                        }
                    } else if (s.endsWith("ls")) {
                        inLs = true;
                    }
                } else if (inLs) {
                    String[] parts = s.split(" ");
                    if (parts[0].equals("dir")) {
                        cwd.addDirectory(parts[1]);
                    } else {
                        cwd.files.add(new File(parts[1], Integer.parseInt(parts[0])));
                    }
                }
            }

            return cwd.getRoot();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }


    static void part1() {
        Directory input = readInput();

        AtomicInteger count = new AtomicInteger();
        input.walk(d -> {
            int size = d.size();
            if (size < 100_000) {
                count.getAndAdd(size);
            }
        });
        System.out.println(count.get());
    }

    static void part2() {
        Directory input = readInput();

        int target = 30_000_000 - (70_000_000 - input.size());
        AtomicInteger closest = new AtomicInteger(Integer.MAX_VALUE);
        input.walk(d -> {
            int size = d.size();
            if (size > target) {
                if (closest.get() > size) {
                    closest.set(size);
                }
            }
        });
        System.out.println(closest.get());
    }

    record File(String name, int size) {}

    static class Directory {
        final String name;
        final List<File> files;
        final List<Directory> directories;
        final Directory parent;

        public Directory(String name, Directory parent) {
            this.name = name;
            this.files = new ArrayList<>();
            this.directories = new ArrayList<>();
            this.parent = parent;
        }

        public Directory addDirectory(String name) {
            Directory newDirectory = new Directory(name, this);
            this.directories.add(newDirectory);
            return newDirectory;
        }

        public Directory getRoot() {
            Directory cwd = this;
            while (cwd.parent != null) {
                cwd = cwd.parent;
            }
            return cwd;
        }

        public Directory cd(String path) {
            if (path.equals("..")) {
                return parent;
            }

            return directories.stream()
                    .filter(d -> d.name.equals(path))
                    .findFirst()
                    .orElseGet(() -> addDirectory(path));
        }

        public void walk(Consumer<Directory> f) {
            f.accept(this);
            directories.forEach(d -> d.walk(f));
        }

        public int size() {
            int fileSize = files.stream().mapToInt(File::size).sum();
            int directorySize = directories.stream().mapToInt(Directory::size).sum();
            return fileSize + directorySize;
        }
    }
}
