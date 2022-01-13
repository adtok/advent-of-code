"""Advent of Code 2015: Day 9"""


from itertools import permutations
from collections import defaultdict
from typing import Callable, DefaultDict, Dict, List


def parse_line(line: str):
    words = line.split()
    src = words[0]
    dest = words[2]
    dist = int(words[4])
    return (src, dest, dist)


def build_graph(input_file: str) -> DefaultDict[str, Dict[str, int]]:
    graph = defaultdict(dict)
    with open(input_file, "r") as file:
        for src, dest, dist in map(parse_line, file):
            graph[src][dest] = dist
            graph[dest][src] = dist
    return graph


def part_one(input_file: str):
    distances = build_graph(input_file)
    cities = list(distances.keys())

    result = min(
        sum(distances[src][dest] for src, dest in zip(route, route[1:]))
        for route in permutations(cities)
    )

    return result


def part_two(input_file: str):
    distances = build_graph(input_file)
    cities = list(distances.keys())

    result = max(
        sum(distances[src][dest] for src, dest in zip(route, route[1:]))
        for route in permutations(cities)
    )

    return result


def solve(func: Callable[[str], int]):
    input_file = "data/09.solution"
    result = func(input_file)
    print(f"The solution for {func.__name__!r} is {result}")


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
