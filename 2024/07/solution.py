import itertools

from typing import Callable, Iterable, Generator


def ADD(a: int, b: int) -> int:
    return a + b


def MULTIPLY(a: int, b: int) -> int:
    return a * b


def CONCATONATION(a: int, b: int) -> int:
    return int(str(a) + str(b))


FILENAME = "input.txt"
OPERATORS = [ADD, MULTIPLY, CONCATONATION]

Equation = tuple[int, list[int]]
Operation = Callable[[int, int], int]


def main():
    with open(FILENAME, "r") as file:
        equations = list(map(parse_line, file))

    part_one(equations=equations)
    part_two(equations=equations)


def part_one(equations: list[Equation]):
    result = sum(
        test_value for test_value, numbers in equations if valid(test_value, numbers)
    )
    print(f"Part one: {result}")


def part_two(equations: list[Equation]):
    result = sum(
        test_value
        for test_value, numbers in equations
        if valid(test_value, numbers, include_concatonation=True)
    )
    print(f"Part two: {result}")


def parse_line(line: str) -> Equation:
    test_value, inputs = line.split(": ")
    result = (int(test_value), list(map(int, inputs.split())))
    return result


def valid(
    test_value: int, numbers: list[int], include_concatonation: bool = False
) -> bool:
    num_pairs = len(numbers) - 1
    if num_pairs < 1:
        return numbers[0] == test_value
    for operations in operator_combinations(
        num_pairs, include_concatonation=include_concatonation
    ):
        result = compute(numbers, operations)
        if result == test_value:
            return True
    return False


def compute(
    numbers: list[int], operations: Iterable[Operation], test_value: int | None = None
) -> int:
    [initial, *rest] = numbers
    result = initial
    for number, operation in zip(rest, operations):
        result = operation(result, number)
        if test_value and result > test_value:
            return result
    return result


def operator_combinations(
    size: int, include_concatonation: bool = False
) -> Generator[Generator[Operation, None, None], None, None]:
    indices = itertools.product(range(2 + include_concatonation), repeat=size)
    yield from (list(OPERATORS[i] for i in combination) for combination in indices)


def valid_faster(test_value: int, numbers: list[int]) -> bool:
    indices = (0, 1, 2)
    [initial, *rest] = numbers
    result = numbers
    # for


if __name__ == "__main__":
    main()
