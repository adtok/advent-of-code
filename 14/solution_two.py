"""
Advent of Code 2021: Day 14 Part 1
tldr:
"""

from __future__ import annotations

from collections import Counter, defaultdict
from io import TextIOWrapper
from typing import DefaultDict, Dict, Iterator, Tuple


Pairs = DefaultDict[str, int]


def process(template: str, insertion_rules: Dict[str, str]) -> str:
    new_template = template[0]

    for i, element in enumerate(template[1:]):
        check = template[i] + element
        inserted_element = insertion_rules.get(check, "")
        insert = inserted_element + element
        new_template += insert

    return new_template


def react(pairs: Pairs, equations: Dict[str, str]) -> Pairs:
    new_pairs = defaultdict(int)

    for pair, count in pairs.items():
        np1, np2 = equations[pair]
        new_pairs[np1] += count
        new_pairs[np2] += count

    return new_pairs


def get_bonds(file: TextIOWrapper) -> Iterator[Tuple[str, str]]:
    for line in file:
        pair, _, bond = line.strip().split()
        yield (pair, bond)


def get_equations(rules: Dict[str, str]) -> Iterator[Tuple[str, str, str]]:
    for pair, bond in rules.items():
        p1 = pair[0] + bond
        p2 = bond + pair[1]
        yield (pair, p1, p2)


def solve(input_file: str) -> int:
    with open(input_file, "r") as file:
        template = file.readline().strip()
        next(file)

        insertion_rules = {pair: bond for pair, bond in get_bonds(file)}

    pairs = [template[i - 1 : i + 1] for i in range(1, len(template))]

    counts = defaultdict(int)

    for pair in pairs:
        counts[pair] += 1


    equations = {pair: (r1, r2) for pair, r1, r2 in get_equations(insertion_rules)}
    for _ in range(40):
        counts = react(counts, equations)

    mapping = defaultdict(int)
    for pair, count in counts.items():
        mapping[pair[0]] += count
    mapping[template[-1]] += 1

    counter = Counter(mapping)

    frequencies = counter.most_common()

    most_common = frequencies[0]
    least_common = frequencies[-1]

    result = most_common[1] - least_common[1]

    print(f"The solution to {input_file!r} is {result}.")

    return result


def main() -> None:
    test_result = solve("input.test")
    test_answer = 2188189693529
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
