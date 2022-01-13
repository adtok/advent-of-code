"""Advent of Code 2015: Day 10"""

from itertools import groupby
from typing import Callable


def look_and_say(number: str, times: int = 1) -> str:
    result = "".join(str(len(list(group))) + digit for digit, group in groupby(number))
    return result if times == 1 else look_and_say(result, times - 1)


def solve(func: Callable[[str], int]):
    input_value = "1321131112"
    result = func(input_value)
    print(f"The solution for {func.__name__!r} is {result}")


def part_one(input_value: str) -> int:
    new_number = look_and_say(input_value, times=40)
    result = len(new_number)
    return result


def part_two(input_value: str) -> int:
    new_number = look_and_say(input_value, times=50)
    result = len(new_number)
    return result


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
