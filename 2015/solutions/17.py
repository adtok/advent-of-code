"""Advent of Code 2015: Day 16"""

from typing import Callable, List
from itertools import combinations


def load_input(input_file: str) -> List[int]:
    with open(input_file, "r") as file:
        data = list(map(int, file))
    return data


def part_one(input_file: str) -> int:
    target_liters = 150
    containers = load_input(input_file)

    result = sum(
        sum(sum(cs) == target_liters for cs in combinations(containers, i + 1))
        for i in range(len(containers))
    )

    return result


def part_two(input_file: str) -> int:
    target_liters = 150
    containers = load_input(input_file)
    
    for i in range(len(containers)):
        valid_combinations = sum(
            sum(cs) == target_liters for cs in combinations(containers, i + 1)
        )
        if valid_combinations:
            result = valid_combinations
            break

    return result


def solve(func: Callable[[str], int]):
    input_file = "data/17.solution"
    result = func(input_file)
    print(f"The solution for {func.__name__!r} is {result}")


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
