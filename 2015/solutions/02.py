"""Advent of Code 2015: Day 2"""

from typing import Callable, List, Tuple


Present = Tuple[int, int, int]


def wrapping_paper_needed(present: Present):
    l, w, h = present
    sides = (l * w, w * h, h * l)
    surface_area = 2 * sum(sides)
    slack = min(sides)
    result = surface_area + slack
    return result

def ribbon_needed(present: Present):
    l, w, h = present
    smallest_perimeter = 2 * min(l + w, w + h, h + l)
    bow = l * w * h
    result = smallest_perimeter + bow
    return result

def parse_line(line: str) -> Present:
    return tuple(map(int, line.split("x")))


def parse_input(input_file: str) -> List[Present]:
    with open(input_file, "r") as file:
        presents = list(map(parse_line, file))
    return presents


def part_one(input_file: str) -> int:
    presents = parse_input(input_file)
    result = sum(map(wrapping_paper_needed, presents))
    return result


def part_two(input_file: str) -> int:
    presents = parse_input(input_file)
    result = sum(map(ribbon_needed, presents))
    return result


def solve(func: Callable[[str], int]):
    input_file = "data/02.solution"
    result = func(input_file)
    print(f"The solution for {func.__name__!r} is {result}")


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
