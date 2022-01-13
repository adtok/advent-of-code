"""Advent of Code 2015: Day 13"""


from dataclasses import dataclass
from collections import defaultdict
from itertools import permutations
from typing import Callable, DefaultDict, Dict, List


def load_graph(input_file):
    graph = defaultdict(dict)

    with open(input_file, "r") as file:
        for line in file:
            values = line.strip().strip(".").split()
            sitter = values[0]
            sign = 1 if values[2] == "gain" else -1
            happiness = int(values[3])
            neighbor = values[-1]
            graph[sitter][neighbor] = happiness * sign

    return graph


def get_maximum_happiness(graph):
    guests = list(graph.keys())
    size = len(guests)

    max_happiness = float("-inf")

    h_l = lambda g, s, i: graph[g][s[i - 1]]
    h_r = lambda g, s, i: graph[g][s[(i + 1) % size]]

    max_happiness = max(
        sum(
            h_l(guest, seating, i) + h_r(guest, seating, i)
            for i, guest in enumerate(seating)
        )
        for seating in permutations(guests)
    )

    return max_happiness


def solve(func: Callable[[str], int]):
    input_value = "data/13.solution"
    result = func(input_value)
    print(f"The solution for {func.__name__!r} is {result}")


def part_one(input_file: str) -> int:
    graph = load_graph(input_file)
    result = get_maximum_happiness(graph)
    return result


def part_two(input_file: str) -> int:
    graph = load_graph(input_file)
    for guest in graph:
        graph[guest]["me"] = 0
    me = {guest: 0 for guest in graph}
    graph["me"] = me
    result = get_maximum_happiness(graph)
    return result


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
