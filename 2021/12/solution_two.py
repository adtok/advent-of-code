"""
Advent of Code 2021: Day 12 Part 1
tldr: Modified depth first search
"""

from collections import defaultdict
from typing import DefaultDict, List, Set


Cave = DefaultDict[str, List[str]]


def is_big(label: str) -> bool:
    """Returns whether or not a cave is large based on its label"""
    return label.isupper()


def walk(
    cave: Cave, current: str, start: str, end: str, visited: Set[str], can_visit_twice: bool = True
) -> int:
    """
    Recursive function to find all paths that walk small caves at most once,
    with the exception of one allowed double-visit
    """
    if current == end:
        return 1

    count = 0

    neighbors = cave[current]

    for neighbor in neighbors:
        if is_big(neighbor) or neighbor not in visited:
            count += walk(cave, neighbor, start, end, visited | {neighbor}, can_visit_twice)
        elif can_visit_twice and neighbor not in {start, end}:
            count += walk(cave, neighbor, start, end, visited | {neighbor}, False)

    return count


def start_walk(cave: Cave, start: str, end: str) -> int:
    """Counts paths from start to finish"""
    return walk(cave=cave, current=start, start=start, end=end, visited={start})


def solve(input_file: str) -> int:
    cave: Cave = defaultdict(list)
    with open(input_file, "r") as file:
        for line in file:
            c1, c2 = line.strip().split("-")
            cave[c1].append(c2)
            cave[c2].append(c1)

    result = start_walk(cave, "start", "end")

    print(f"The solution for {input_file!r} is {result}.")

    return result


def main() -> None:
    test_result_one = solve("input.test_one")
    test_answer_one = 36
    assert test_result_one == test_answer_one
    test_result_two = solve("input.test_two")
    test_answer_two = 103
    assert test_result_two == test_answer_two
    test_result_three = solve("input.test_three")
    test_answer_three = 3509
    assert test_result_three == test_answer_three
    solve("input.solution")


if __name__ == "__main__":
    main()
