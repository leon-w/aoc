package utils;

import java.util.Objects;

public class Range {
    public final int start;
    public final int end;

    public Range(int start, int end) {
        // end is not included
        this.start = start;
        this.end = end;
    }

    public int size() {
        return end - start - 1;
    }

    @Override
    public String toString() {
        return String.format("[%d; %d)", start, end);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Range range = (Range) o;
        return start == range.start && end == range.end;
    }

    @Override
    public int hashCode() {
        return Objects.hash(start, end);
    }
}
