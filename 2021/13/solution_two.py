"""
Advent of Code 2021: Day 13 Part 2
tldr: multiple folds and print letters
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


def show_paper(points: Dots) -> None:
    x_max = max(x for _, x in points)
    y_max = max(y for y, _ in points)

    for y in range(y_max + 1):
        print("".join(".#"[(y, x) in points] for x in range(x_max + 1)))


def solve(input_file: str) -> None:
    with open(input_file, "r") as file:
        pair_data, fold_data = file.read().split("\n\n")
        points = set(map(parse_point, pair_data.split("\n")))
        folds = list(map(parse_fold, fold_data.split("\n")))

    direction, fold_val = folds[0]

    for direction, fold_val in folds:
        points = fold_points(points, direction, fold_val)

    show_paper(points)


def main():
    solve("input.test")
    solve("input.solution")


if __name__ == "__main__":
    main()
