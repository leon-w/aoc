package y2022;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;

public class Day21 {
    public static void main(String[] args) {
        System.out.println(">>> Part 1 <<<");
        part1();
        System.out.println("==============");
        System.out.println();
        System.out.println(">>> Part 2 <<<");
        part2();
        System.out.println("==============");
    }

    static List<Monkey> readInput() {
        try (Stream<String> stream = Files.lines(Paths.get("inputs/21.txt"))) {
            return stream.map(s -> {
                String[] parts = s.split(": ");
                String name = parts[0];
                parts = parts[1].split(" ");
                if (parts.length > 1) {
                    return new MonkeyOperation(name, parts[0], parts[2], parts[1].charAt(0));
                } else {
                    return new MonkeyConstant(name, Integer.parseInt(parts[0]));
                }
            }).toList();
        } catch (IOException e) {
            throw new RuntimeException("Failed to read input: " + e.getMessage());
        }
    }

    static void part1() {
        List<Monkey> monkeys = readInput();

        MonkeySolver solver = new MonkeySolver(monkeys);

        System.out.println(solver.getValue("root"));
    }

    static void part2() {
        List<Monkey> monkeys = readInput();

        MonkeySolver solver = new MonkeySolver(monkeys);

        MonkeyOperation rootMonkey = (MonkeyOperation) solver.monkeyMap.get("root");

        Expression left = solver.getSimplifiedExpression(rootMonkey.leftOperand);
        Expression right = solver.getSimplifiedExpression(rootMonkey.rightOperand);

        // we know that X (the variable we are trying to solve for)
        // occurs only once on the left side and the right side is a constant

        long targetVal = ((ConstantExpression) right).constant;
        Expression eq = left;
        while (eq.getClass() == BinaryExpression.class) {
            BinaryExpression eqBinary = (BinaryExpression) eq;
            Expression eqLeft = eqBinary.left;
            Expression eqRight = eqBinary.right;

            boolean leftIsConstant = eqLeft.getClass() == ConstantExpression.class;
            long constVal = ((ConstantExpression) (leftIsConstant ? eqLeft : eqRight)).constant;

            targetVal = switch (eqBinary.operand) {
                case '+' -> targetVal - constVal;
                case '*' -> targetVal / constVal;
                case '-' -> leftIsConstant ? (constVal - targetVal) : (targetVal + constVal);
                case '/' -> leftIsConstant ? (constVal / targetVal) : (targetVal * constVal);
                default -> throw new RuntimeException("Invalid operator");
            };

            eq = leftIsConstant ? eqRight : eqLeft;
        }

        System.out.println(targetVal);
    }

    abstract static class Monkey {
        final String name;

        Monkey(String name) {
            this.name = name;
        }

        boolean isConstant() {
            return getClass() == MonkeyConstant.class;
        }
    }

    static class MonkeyConstant extends Monkey {
        final long constant;

        MonkeyConstant(String name, long constant) {
            super(name);
            this.constant = constant;
        }

        @Override
        public String toString() {
            return String.format("%s(%d)", name, constant);
        }
    }

    static class MonkeyOperation extends Monkey {
        final String leftOperand;
        final String rightOperand;
        final char operator;

        MonkeyOperation(String name, String leftOperand, String rightOperand, char operator) {
            super(name);
            this.leftOperand = leftOperand;
            this.rightOperand = rightOperand;
            this.operator = operator;
        }

        long compute(long left, long right) {
            return switch (operator) {
                case '+' -> left + right;
                case '-' -> left - right;
                case '*' -> left * right;
                case '/' -> left / right;
                default -> throw new RuntimeException("Invalid operator");
            };
        }

        @Override
        public String toString() {
            return String.format("%s(%s %c %s)", name, leftOperand, operator, rightOperand);
        }
    }

    static class MonkeySolver {
        Map<String, Monkey> monkeyMap = new HashMap<>();

        MonkeySolver(List<Monkey> monkeys) {
            for (Monkey m : monkeys) {
                monkeyMap.put(m.name, m);
            }
        }

        long getValue(String name) {
            Monkey m = monkeyMap.get(name);

            if (m.isConstant()) {
                MonkeyConstant mc = (MonkeyConstant) m;
                return mc.constant;
            }

            MonkeyOperation mo = (MonkeyOperation) m;
            long leftValue = getValue(mo.leftOperand);
            long rightValue = getValue(mo.rightOperand);
            return mo.compute(leftValue, rightValue);
        }

        Expression getSimplifiedExpression(String name) {
            Monkey m = monkeyMap.get(name);

            if (m.name.equals("humn")) return new VariableExpression();

            if (m.isConstant()) return new ConstantExpression(((MonkeyConstant) m).constant);


            MonkeyOperation mo = (MonkeyOperation) m;
            Expression left = getSimplifiedExpression(mo.leftOperand);
            Expression right = getSimplifiedExpression(mo.rightOperand);

            if (left.getClass() == ConstantExpression.class && right.getClass() == ConstantExpression.class) {
                long leftVal = ((ConstantExpression) left).constant;
                long rightVal = ((ConstantExpression) right).constant;
                return new ConstantExpression(mo.compute(leftVal, rightVal));
            }

            return new BinaryExpression(left, right, mo.operator);
        }
    }

    abstract static class Expression {}

    static class VariableExpression extends Expression {
        @Override
        public String toString() {
            return "X";
        }
    }

    static class ConstantExpression extends Expression {
        final long constant;

        ConstantExpression(long constant) {
            this.constant = constant;
        }

        @Override
        public String toString() {
            return Long.toString(constant);
        }
    }

    static class BinaryExpression extends Expression {
        final Expression left;
        final Expression right;
        final char operand;

        BinaryExpression(Expression left, Expression right, char operand) {
            this.left = left;
            this.right = right;
            this.operand = operand;
        }

        @Override
        public String toString() {
            return String.format("(%s %c %s)", left, operand, right);
        }
    }
}
