"""
Advent of Code 2021: Day 25
tldr: moving sea cucumbers
"""

from __future__ import annotations
from typing import List, Tuple
from copy import deepcopy

import itertools


EMPTY = 0
SOUTH = 1
EAST = 2

MOVE_SOUTH = (1, 0)
MOVE_EAST = (0, 1)


def _parse_input(input_file: str) -> Tuple[Seafloor, int, int]:
    mapping = {".": EMPTY, "v": SOUTH, ">": EAST}
    with open(input_file, "r") as file:
        seafloor = [list(map(mapping.get, line.strip())) for line in file.readlines()]
    return seafloor


class Seafloor:
    def __init__(self, data: List[List[int]]):
        self.data = data
        self.height = len(data)
        self.width = len(data[0])
        self.steps = 0
        self.history = [self.serialize()]

    @classmethod
    def from_file(cls, input_file: str) -> Seafloor:
        data = _parse_input(input_file)
        return cls(data=data)

    def serialize(self) -> str:
        mapping = {EMPTY: ".", SOUTH: "v", EAST: ">"}
        result = "\n".join("".join(map(mapping.get, row)) for row in self.data)
        return result

    def show(self):
        serialized = self.serialize()
        print(serialized)

    def move_cucumber_group(self, group_number: int) -> None:
        moved = False
        new_data = deepcopy(self.data)
        for y, x in itertools.product(range(self.height), range(self.width)):
            value = self.data[y][x]
            if value != group_number or value == EMPTY:
                continue
            dy, dx = MOVE_SOUTH if value == SOUTH else MOVE_EAST
            new_y = (y + dy) % self.height
            new_x = (x + dx) % self.width
            if self.data[new_y][new_x] == EMPTY:
                new_data[y][x] = EMPTY
                new_data[new_y][new_x] = value
                moved = True

        self.data = new_data

        return moved

    def step(self):
        east_moves = self.move_cucumber_group(EAST)
        south_moves = self.move_cucumber_group(SOUTH)
        serialized = self.serialize()
        self.history += [serialized]

        moves = east_moves or south_moves

        self.steps += 1

        return moves

    def run(self, verbose: bool = False):
        while self.step():
            if verbose:
                print(f"After step {self.steps}\n")
                self.show()
        print(f"No change after {self.steps} steps")
        return self.steps


def part_one(input_file: str):
    seafloor = Seafloor.from_file(input_file)
    seafloor.run(verbose=False)


def main():
    part_one("input.test")
    part_one("input.solution")


if __name__ == "__main__":
    main()
