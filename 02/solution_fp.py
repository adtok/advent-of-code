"""
Advent of Code 2021: Day 02 Part 2
tldr: find ending position with a twist
"""

from typing import Tuple
from functools import reduce


Line = Tuple[str, int]
State = Tuple[int, int, int]


def EMPTY_STATE() -> State:
    return (0, 0, 0)


def parse_line(line: str) -> Tuple[str, int]:
    direction, magnitude = line.split()
    return direction, int(magnitude)


def state_from_line(line: Line) -> State:
    direction, magnitude = line
    factories = {
        "forward": (magnitude, 0, 0),
        "down": (0, 0, magnitude),
        "up": (0, 0, -magnitude),
    }
    state = factories.get(direction, EMPTY_STATE())
    return state


def fold(state1: State, state2: State) -> State:
    hor1, ver1, aim1 = state1
    hor2, ver2, aim2 = state2
    return (hor1 + hor2), (ver1 + ver2 + (aim1 * hor2)), (aim1 + aim2)


def main(input_file: str) -> None:
    with open(input_file, "r") as file:
        final_state = reduce(
            fold, map(state_from_line, map(parse_line, file)), EMPTY_STATE()
        )

    hor, ver, _ = final_state
    result = ver * hor
    print(result)


if __name__ == "__main__":
    input_file = "input.solution"
    main(input_file)
