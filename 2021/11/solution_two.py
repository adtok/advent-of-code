"""
Advent of Code 2021: Day 11 Part 2
tldr:
"""


from dataclasses import dataclass
from typing import List, Optional, Tuple

Point = Tuple[int, int]


DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def in_bounds(point):
    y, x = point
    return 0 <= y <= 9 and 0 <= x <= 9


def get_neighbors(point: Point):
    y, x = point
    return [(y + dy, x + dx) for dy, dx in DIRS if in_bounds((y + dy, x + dx))]


@dataclass
class Octopus:
    energy_level: int
    y: int
    x: int
    flashed: bool = False

    @property
    def neighbors(self):
        return get_neighbors((self.y, self.x))

    def increment(self):
        flash_neighbors = False
        self.energy_level += 1
        if self.energy_level > 9 and not self.flashed:
            flash_neighbors = True
            self.flashed = True
        return flash_neighbors

    def cleanup(self):
        if self.energy_level > 9:
            self.energy_level = 0
            self.flashed = False
            return True
        return False


@dataclass
class Step:
    number: int
    flashes: int
    energy_level_map: str


class Grid:
    def __init__(self, energy_levels: List[List[int]]) -> None:
        data = [
            [
                Octopus(energy_level=energy_level, y=y, x=x)
                for x, energy_level in enumerate(row)
            ]
            for y, row in enumerate(energy_levels)
        ]
        self.octopuses = data
        self.height = len(data)
        self.width = len(data[0])
        self.size = self.width * self.height
        self.flash_count = 0
        self.step_count = 0
        self.steps: List[Step] = [
            Step(number=0, flashes=0, energy_level_map=self.energy_levels)
        ]

    @property
    def energy_levels(self) -> str:
        els = "\n".join(
            "".join(str(o.energy_level) for o in row) for row in self.octopuses
        )
        return els

    def step(self, verbose=False) -> None:
        stack: List[Point] = []
        for row in range(self.height):
            for col in range(self.height):
                o = self.octopuses[row][col]
                should_flash = o.increment()
                if should_flash:
                    stack.extend(o.neighbors)

        while stack:
            y, x = stack.pop(0)
            o = self.octopuses[y][x]
            should_flash = o.increment()
            if should_flash:
                stack.extend(o.neighbors)

        flashes = 0
        for row in range(self.height):
            for col in range(self.width):
                flashed = self.octopuses[row][col].cleanup()
                flashes += flashed
        self.step_count += 1
        self.steps.append(
            Step(
                number=self.step_count,
                flashes=flashes,
                energy_level_map=self.energy_levels,
            )
        )
        self.flash_count += flashes
        if verbose:
            print(f"\nAfter step {self.step_count}:\n{self.energy_levels}")
        return flashes

    def get_octopus(self, p: Point):
        y, x = p
        return self.octopuses[y][x]


def solve(input_file: str) -> int:
    with open(input_file, "r") as file:
        energy_levels = [list(map(int, line.strip())) for line in file]
    grid = Grid(energy_levels)

    print("Before any steps:")
    print(grid.energy_levels)

    flashes = None
    while flashes != grid.size:
        flashes = grid.step(verbose=True)

    result = grid.step_count
    print(f"The solution to {input_file!r} is {result}.")
    return result


def main():
    test_result = solve("input.test")
    test_answer = 195
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
