package utils;


import java.util.Iterator;
import java.util.function.Function;

public class Matrix2d {
    public final int w;
    public final int h;
    private final int[][] data;

    public Matrix2d(int[][] data) {
        this.w = data[0].length;
        this.h = data.length;
        this.data = data;
    }

    public Matrix2d(int w, int h) {
        this.w = w;
        this.h = h;
        this.data = new int[h][w];
    }

    public Matrix2d zerosLike() {
        return new Matrix2d(w, h);
    }

    public Matrix2d copy() {
        int[][] clonedData = data.clone();
        for (int i = 0; i < clonedData.length; i++) {
            clonedData[i] = data[i].clone();
        }
        return new Matrix2d(clonedData);
    }

    public int get(int x, int y) {
        return data[y][x];
    }

    public int get(Point2d p) {
        return get(p.x, p.y);
    }

    public int set(int x, int y, int val) {
        this.data[y][x] = val;
        return val;
    }

    public int set(Point2d p, int val) {
        return set(p.x, p.y, val);
    }

    public int add(int x, int y, int val) {
        this.data[y][x] += val;
        return val;
    }

    public int add(Point2d p, int val) {
        return add(p.x, p.y, val);
    }

    public int sum() {
        int acc = 0;
        for (int y = 0; y < h; y++) {
            for (int x = 0; x < w; x++) {
                acc += data[y][x];
            }
        }
        return acc;
    }

    public int count(int val) {
        int c = 0;
        for (int y = 0; y < h; y++) {
            for (int x = 0; x < w; x++) {
                if (data[y][x] == val) {
                    c++;
                }
            }
        }
        return c;
    }

    public void fill(int val) {
        for (int y = 0; y < h; y++) {
            for (int x = 0; x < w; x++) {
                data[y][x] = val;
            }
        }
    }

    public Matrix2d subMatrix(int startX, int endX, int startY, int endY) {
        Matrix2d sub = new Matrix2d(endX - startX, endY - startY);
        for (int x = startX; x < endX; x++) {
            for (int y = startY; y < endY; y++) {
                sub.data[y - startY][x - startX] = data[y][x];
            }
        }
        return sub;
    }

    public boolean isValidPosition(Point2d p) {
        return p.x >= 0 && p.x < w && p.y >= 0 && p.y < h;
    }

    public Iterable<Point2d> iterateCoords() {
        return () -> new Iterator<>() {
            private int index = 0;

            @Override
            public boolean hasNext() {
                return index < w * h;
            }

            @Override
            public Point2d next() {
                Point2d p = new Point2d(index % w, index / w);
                index++;
                return p;
            }
        };

    }

    public String toString() {
        return toString(null);
    }

    public String toString(Function<Integer, String> formatter) {
        StringBuilder sb = new StringBuilder();
        String[][] formatted = new String[h][w];
        int maxLen = 0;
        for (int y = 0; y < h; y++) {
            for (int x = 0; x < w; x++) {
                String s = formatter == null ? String.format("%d", data[y][x]) : formatter.apply(data[y][x]);
                formatted[y][x] = s;
                maxLen = Math.max(maxLen, s.length());
            }
        }
        for (int y = 0; y < h; y++) {
            for (int x = 0; x < w; x++) {
                sb.append(String.format("%-" + maxLen + "s", formatted[y][x]));
                if (x != w - 1 && formatter == null) {
                    sb.append(" ");
                }
            }
            if (y != h - 1) {
                sb.append("\n");
            }
        }
        return sb.toString();
    }
}
