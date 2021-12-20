"""
Advent of Code 2021: Day 18 Part 1
tldr: pairs and reducing
"""

from __future__ import annotations
from dataclasses import dataclass
from functools import reduce
from typing import List, Tuple


@dataclass
class Pair:
    value: int
    depth: int


FlatList = List[Pair]


def parse_line(line: str) -> List[Pair]:
    flat_list = []
    depth = 0
    for char in line:
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
        elif char.isdigit():
            flat_list.append(Pair(value=int(char), depth=depth))
    return flat_list


def parse_input(input_file: str) -> List[List[Pair]]:
    with open(input_file, "r") as file:
        result = list(map(parse_line, file))
    return result


def explode(pairs: FlatList) -> Tuple[bool, FlatList]:
    for i, (pair1, pair2) in enumerate(zip(pairs, pairs[1:])):
        if pair1.depth < 5 or pair1.depth != pair2.depth:
            continue
        if i > 0:
            pairs[i - 1].value += pair1.value
        if i < len(pairs) - 2:
            pairs[i + 2].value += pair2.value
        return True, pairs[:i] + [Pair(value=0, depth=pair1.depth - 1)] + pairs[i + 2 :]
    return False, pairs


def split(pairs: FlatList) -> Tuple[bool, FlatList]:
    for i, pair in enumerate(pairs):
        if pair.value < 10:
            continue
        down = pair.value // 2
        up = pair.value - down
        return (
            True,
            pairs[:i]
            + [
                Pair(value=down, depth=pair.depth + 1),
                Pair(value=up, depth=pair.depth + 1),
            ]
            + pairs[i + 1 :],
        )
    return False, pairs


def add(p1: FlatList, p2: FlatList) -> FlatList:
    pairs = [Pair(value=p.value, depth=p.depth + 1) for p in p1 + p2]
    while True:
        change, pairs = explode(pairs)
        if change:
            continue
        change, pairs = split(pairs)
        if not change:
            break
    return pairs


def magnitude(pairs: FlatList) -> 0:
    while len(pairs) > 1:
        for i, (pair1, pair2) in enumerate(zip(pairs, pairs[1:])):
            if pair1.depth != pair2.depth:
                continue
            value = 3 * pair1.value + 2 * pair2.value
            depth = pair1.depth - 1
            pairs = pairs[:i] + [Pair(value=value, depth=depth)] + pairs[i + 2 :]
            break
    return pairs[0].value


def solve(input_file: str) -> int:
    pairs = parse_input(input_file)
    result = magnitude(reduce(add, pairs))

    print(f"The solution for {input_file!r} is {result}.")

    return result


def main():
    test_result = solve("input.test")
    test_answer = 4140
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
