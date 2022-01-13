"""Advent of Code 2015: Day 20"""

from itertools import count
from typing import Callable, List


def get_factors(n: int) -> List[int]:
    divisors = []
    sqrt = int(n ** 0.5) + 1
    for i in range(1, sqrt):
        if n % i == 0:
            divisors.append(i)
            divisors.append(n // i)
    return divisors


def calculate_presents(house: int, presents_per_elf: int, upper_limit: int = 0):
    factors = get_factors(house)
    if upper_limit:
        factors = list(filter(lambda f: f <= upper_limit, factors))
        # print(factors)

    return presents_per_elf * sum(factors)


def find_lowest_house(value: int, ppe: int, upper_limit: int = 0):
    step = 6
    for i in count(step, step):
        if calculate_presents(i, ppe, upper_limit=upper_limit) >= value:
            lowest = i
            for j in count(1):
                if calculate_presents(i - j, ppe, upper_limit=upper_limit) >= value:
                    lowest = i - j
                else:
                    break
            return lowest
    return -1


def part_one(input_value: int) -> int:
    result = find_lowest_house(input_value, 10)
    return result


def part_two(input_value: int) -> int:
    result = find_lowest_house(input_value, 11, upper_limit=50)
    return result


def solve(func: Callable[[int], int]):
    input_value = 34_000_000
    result = func(input_value)
    print(f"The solution for {func.__name__!r} is {result}")


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
