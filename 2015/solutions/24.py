"""Advent of Code 2015: Day 24"""

import itertools
import functools
from typing import Callable, List


def parse_input(input_file: str) -> List[int]:
    """Parses a file of line-separated integers into a list"""
    with open(input_file, "r") as file:
        data = list(map(int, file))
    return data


def product(weights: List[int]) -> int:
    """Returns the product of a list of integers"""
    return functools.reduce(lambda a, b: a * b, weights, 1)


def target_sum(weights: List[int], num_groups: int) -> int:
    """Determines the weight a group of presents needs to be"""
    return sum(weights) // num_groups


def minimum_quantum_entanglement(weights: List[int], num_groups: int):
    """Determines the minimum quantum entanglement"""
    num_presents = len(weights)
    target = target_sum(weights, num_groups)
    min_qe = float("inf")
    for group_size in itertools.count(1):
        found = False
        for combination in itertools.combinations(weights, group_size):
            if sum(combination) != target:
                continue
            found = True
            quantum_entanglement = product(combination)
            min_qe = min(min_qe, quantum_entanglement)

        if found or group_size == num_presents:
            break

    result = min_qe
    return result


def part_one(input_file: str) -> int:
    weights = parse_input(input_file)
    result = minimum_quantum_entanglement(weights, 3)
    return result


def part_two(input_file: str) -> int:
    weights = parse_input(input_file)
    result = minimum_quantum_entanglement(weights, 4)
    return result


def solve(func: Callable[[str], int]):
    input_file = "data/24.solution"
    result = func(input_file)
    print(f"The solution for {func.__name__!r} is {result}")


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
