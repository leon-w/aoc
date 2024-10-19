package utils;

import java.util.Objects;

public class Point2d {
    public static Point2d UP = new Point2d(0, -1);
    public static Point2d DOWN = new Point2d(0, 1);
    public static Point2d LEFT = new Point2d(-1, 0);
    public static Point2d RIGHT = new Point2d(1, 0);
    public static Point2d[] ALL_DIRS = new Point2d[]{UP, RIGHT, DOWN, LEFT};

    public static Point2d N = new Point2d(0, -1);
    public static Point2d NE = new Point2d(1, -1);
    public static Point2d E = new Point2d(1, 0);
    public static Point2d SE = new Point2d(1, 1);
    public static Point2d S = new Point2d(0, 1);
    public static Point2d SW = new Point2d(-1, 1);
    public static Point2d W = new Point2d(-1, 0);
    public static Point2d NW = new Point2d(-1, -1);
    public static Point2d[] ALL_DIRS_FULL = new Point2d[]{N, NE, E, SE, S, SW, W, NW};

    public int x;
    public int y;

    public Point2d(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public Point2d add(Point2d direction) {
        return new Point2d(x + direction.x, y + direction.y);
    }

    public Point2d addI(Point2d direction) {
        this.x += direction.x;
        this.y += direction.y;
        return this;
    }

    public Point2d copy() {
        return new Point2d(x, y);
    }

    public Point2d flip() {
        return new Point2d(y, x);
    }

    public int manhattanDistance(Point2d other) {
        return Math.abs(x - other.x) + Math.abs(y - other.y);
    }

    @Override
    public String toString() {
        return String.format("(%d, %d)", x, y);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Point2d point2d = (Point2d) o;
        return x == point2d.x && y == point2d.y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }
}

