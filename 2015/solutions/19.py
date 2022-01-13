"""Advent of Code 2015: Day 19"""


from collections import defaultdict
from typing import Callable, DefaultDict, Dict, Generator, List, Set, Tuple


Replacements = Dict[str, List[str]]


def load_data(input_file: str) -> Tuple[str, Replacements]:
    rules = DefaultDict(list)
    with open(input_file, "r") as file:
        *replacements, _, molecule = map(str.strip, file.readlines())
    for rule in replacements:
        start, end = rule.split(" => ")
        rules[start] += [end]
    return molecule, rules


def load_data_part_two(input_file: str) -> Tuple[str, List[Tuple[str, str]]]:
    rules = DefaultDict(list)
    with open(input_file, "r") as file:
        *replacements, _, molecule = map(str.strip, file.readlines())
    rules = [rule.split(" => ") for rule in replacements]
    return molecule, rules


def nth_replacement(string: str, substring: str, replacement: str, n: int) -> str:
    find = string.find(substring)
    i = find != -1
    while find != -1 and i != n:
        find = string.find(substring, find + 1)
        i += 1
    if i == n:
        return string[:find] + replacement + string[find + len(substring) :]
    return string


def reactions(molecule: str, rules: Replacements) -> Generator:
    new_molecules = set()
    for chemical, replacements in rules.items():
        for n in range(1, molecule.count(chemical) + 1):
            for replacement in replacements:
                new_molecule = nth_replacement(molecule, chemical, replacement, n)
                new_molecules |= {new_molecule}
    yield from new_molecules


def part_one(input_file: str) -> int:
    molecule, rules = load_data(input_file)
    new_molecules = set(reactions(molecule, rules))

    result = len(new_molecules)
    return result


def part_two(input_file: str) -> int:
    steps = 0
    curr, original_rules = load_data_part_two(input_file)

    rules = original_rules.copy()

    while curr != "e":
        try:
            f = max(rules, key=lambda r: len(r[1]))
        except:
            rules = original_rules.copy()
            f = max(rules, key=lambda r: len(r[1]))
        before, after = f
        new = curr.replace(after, before, 1)
        if new != curr:
            steps += 1
        else:
            rules.remove(f)
        curr = new

    result = steps

    return result


def solve(func: Callable[[str], int]):
    input_file = "data/19.solution"
    result = func(input_file)
    print(f"The solution for {func.__name__!r} is {result}")


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
