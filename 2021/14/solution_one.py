"""
Advent of Code 2021: Day 14 Part 1
tldr:
"""

from __future__ import annotations

from collections import Counter
from io import TextIOWrapper
from typing import Dict


def process(template: str, insertion_rules: Dict[str, str]) -> str:
    new_template = template[0]

    for i, element in enumerate(template[1:]):
        check = template[i] + element
        inserted_element = insertion_rules.get(check, "")
        insert = inserted_element + element
        new_template += insert

    return new_template


def get_bonds(file: TextIOWrapper):
    for line in file:
        pair, _, bond = line.strip().split()
        yield (pair, bond)


def solve(input_file: str) -> int:
    with open(input_file, "r") as file:
        template = file.readline().strip()
        next(file)

        insertion_rules = {pair: bond for pair, bond in get_bonds(file)}

    for _ in range(10):
        new_template = process(template, insertion_rules)
        template = new_template

    frequencies = Counter(template).most_common()

    most_common = frequencies[0]
    least_common = frequencies[-1]

    result = most_common[1] - least_common[1]

    print(f"The solution to {input_file!r} is {result}.")

    return result


def main() -> None:
    test_result = solve("input.test")
    test_answer = 1588
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
