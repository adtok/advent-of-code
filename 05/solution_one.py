"""
Advent of Code 2021: Day 05 Part 1
tldr: 
"""


from collections import defaultdict
from typing import List


def parse_line(line: str) -> List[int]:
    p1, _, p2 = line.split()
    x1, y1 = list(map(int, p1.split(",")))
    x2, y2 = list(map(int, p2.split(",")))
    return x1, y1, x2, y2


def solve(input_file: str) -> int:
    points = defaultdict(int)
    with open(input_file, "r") as file:
        for line in file:
            x1, y1, x2, y2 = parse_line(line)
            if x1 != x2 and y1 != y2:
                continue
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    points[(x, y)] += 1

    result = sum(count > 1 for count in points.values())
    print(f"The answer for {input_file!r} is {result}.")
    return result


def main():
    test_result = solve("input.test")
    test_answer = 5
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
