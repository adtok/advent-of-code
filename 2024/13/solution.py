from fractions import Fraction

EXAMPLE = "example.txt"
INPUT = "input.txt"

ADJUSTMENT = 10_000_000_000_000

Vec2 = tuple[Fraction, Fraction]
Matrix = tuple[Vec2, Vec2]
Button = Vec2
Prize = Vec2
Machine = tuple[Button, Button, Prize]


def main() -> None:
    part_one()
    part_two()


def part_one() -> None:
    machines = parse(INPUT)
    solutions = (solve(machine) for machine in machines)
    costs = (3 * a + 1 * b for a, b in solutions)
    result = sum(costs)
    print(f"Part one: {result}")


def part_two() -> None:
    machines = parse(INPUT, adjustment=ADJUSTMENT)
    solutions = (solve(machine) for machine in machines)
    costs = (3 * a + 1 * b for a, b in solutions)
    result = sum(costs)
    print(f"Part two: {result}")


def parse(filename: str, adjustment: int = 0) -> list[Machine]:
    with open(filename, "r") as file:
        raw_machines = file.read().strip().split("\n\n")
    result = [parse_machine(machine, adjustment=adjustment) for machine in raw_machines]
    return result


def parse_machine(raw_machine: str, adjustment: int = 0) -> Machine:
    [raw_a, raw_b, raw_p] = raw_machine.split("\n")
    button_a = parse_button(raw_a)
    button_b = parse_button(raw_b)
    prize = parse_prize(raw_p, adjustment=adjustment)
    return (button_a, button_b, prize)


def parse_button(raw_button: str) -> Button:
    [_, ds] = raw_button.split(": ")
    [raw_x, raw_y] = ds.split(", ")
    x = Fraction(raw_x.split("+")[1])
    y = Fraction(raw_y.split("+")[1])
    result = (x, y)
    return result


def parse_prize(raw_prize: str, adjustment: int = 0) -> Prize:
    [_, ds] = raw_prize.split(": ")
    [raw_x, raw_y] = ds.split(", ")
    x = Fraction(raw_x.split("=")[1])
    y = Fraction(raw_y.split("=")[1])
    result = (x + adjustment, y + adjustment)
    return result


def solve(machine: Machine) -> Vec2:
    button_a, button_b, prize = machine
    a_x, a_y = button_a
    b_x, b_y = button_b
    m = ((a_x, b_x), (a_y, b_y))
    m_ = inverse(m)
    a, b = mult(m_, prize)
    result = (a, b)
    # print(
    #     machine,
    #     (a, b),
    #     (a.numerator % a.denominator == 0, b.numerator % b.denominator == 0),
    #     result,
    # )
    if a.numerator % a.denominator == 0 and b.numerator % b.denominator == 0:
        return result
    return (0, 0)


def inverse(m: Matrix) -> Matrix:
    (a, b), (c, d) = m
    determinant = Fraction(1, (a * d - b * c))
    a_ = d * determinant
    b_ = -b * determinant
    c_ = -c * determinant
    d_ = a * determinant
    return ((a_, b_), (c_, d_))


def matrix_mult(m_a: Matrix, m_b: Matrix) -> Matrix:
    (a_11, a_12), (a_21, a_22) = m_a
    (b_11, b_12), (b_21, b_22) = m_b
    c_11 = a_11 * b_11 + a_12 * b_21
    c_12 = a_11 * b_12 + a_12 * b_22
    c_21 = a_21 * b_11 + a_22 * b_21
    c_22 = a_21 * b_12 + a_22 * b_22
    return ((c_11, c_12), (c_21, c_22))


def mult(m: Matrix, v: Vec2) -> Vec2:
    (m_11, m_12), (m_21, m_22) = m
    (v_1, v_2) = v
    r_1 = m_11 * v_1 + m_12 * v_2
    r_2 = m_21 * v_1 + m_22 * v_2
    result = (r_1, r_2)
    return result


if __name__ == "__main__":
    main()
