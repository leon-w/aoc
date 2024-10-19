package utils;

import java.util.Objects;

public class Point3d {
    public static Point3d UP = new Point3d(0, 0, -1);
    public static Point3d DOWN = new Point3d(0, 0, 1);
    public static Point3d FORWARD = new Point3d(0, -1, 0);
    public static Point3d BACKWARD = new Point3d(0, 1, 0);
    public static Point3d LEFT = new Point3d(-1, 0, 0);
    public static Point3d RIGHT = new Point3d(1, 0, 0);
    public static Point3d[] ALL_DIRS = new Point3d[]{UP, DOWN, FORWARD, BACKWARD, LEFT, RIGHT};

    public int x;
    public int y;
    public int z;

    public Point3d(int x, int y, int z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    public Point3d add(Point3d direction) {
        return new Point3d(x + direction.x, y + direction.y, z + direction.z);
    }

    public Point3d addI(Point3d direction) {
        this.x += direction.x;
        this.y += direction.y;
        this.z += direction.z;
        return this;
    }

    public Point3d copy() {
        return new Point3d(x, y, z);
    }

    public int manhattanDistance(Point3d other) {
        return Math.abs(x - other.x) + Math.abs(y - other.y) + Math.abs(z - other.z);
    }

    @Override
    public String toString() {
        return String.format("(%d, %d, %d)", x, y, z);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Point3d point2d = (Point3d) o;
        return x == point2d.x && y == point2d.y && z == point2d.z;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y, z);
    }
}

