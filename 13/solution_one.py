"""
Advent of Code 2021: Day 13 Part 1
tldr: a single fold
"""


from typing import Set, Tuple


Point = Tuple[int, int]  # (y, x)
Dots = Set[Point]
Fold = Tuple[str, int]


def parse_point(line: str) -> Point:
    x, y = line.split(",")
    return (int(y), int(x))


def parse_fold(line: str) -> Fold:
    *_, data = line.split(" ")
    direction, value = data.split("=")
    return (direction, int(value))


def fold_y(points: Dots, fold_val: int) -> Dots:
    return {(2 * fold_val - y, x) if y > fold_val else (y, x) for y, x in points}


def fold_x(points: Dots, fold_val: int) -> Dots:
    return {(y, 2 * fold_val - x) if x > fold_val else (y, x) for y, x in points}


def fold_points(points: Dots, direction: str, fold_val: int) -> Dots:
    return fold_x(points, fold_val) if direction == "x" else fold_y(points, fold_val)


def solve(input_file: str) -> int:
    with open(input_file, "r") as file:
        pair_data, fold_data = file.read().split("\n\n")
        points = set(map(parse_point, pair_data.split("\n")))
        folds = list(map(parse_fold, fold_data.split("\n")))

    direction, fold_val = folds[0]

    points = fold_points(points, direction, fold_val)

    result = len(points)
    print(f"The solution to {input_file!r} is {result}.")

    return result


def main():
    test_result = solve("input.test")
    test_answer = 17
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
