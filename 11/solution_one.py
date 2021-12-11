"""
Advent of Code 2021: Day 11 Part 1
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
            


class Grid:
    def __init__(self, input_file: str) -> None:
        with open(input_file, "r") as file:
            data = [
                [
                    Octopus(energy_level=energy_level, y=row, x=col)
                    for col, energy_level in enumerate(map(int, line.strip()))
                ]
                for row, line in enumerate(file)
            ]
        self.octopuses = data
        self.height = len(data)
        self.width = len(data[0])
        self.flash_count = 0

    @property
    def energy_levels(self) -> str:
        els = "\n".join(
            "".join(str(o.energy_level) for o in row) for row in self.octopuses
        )
        return els

    def step(self) -> None:
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
        
        for row in range(self.height):
            for col in range(self.width):
                flashed = self.octopuses[row][col].cleanup()
                self.flash_count += flashed
        


    def get_octopus(self, p: Point):
        y, x = p
        return self.octopuses[y][x]


def solve(input_file: str) -> int:
    grid = Grid(input_file)
    
    print("Before any steps:")
    print(grid.energy_levels)

    for step in range(100):
        print()
        grid.step()
        print(f"After step {step+1}:")
        print(grid.energy_levels)


    result = grid.flash_count
    print(f"The solution to {input_file!r} is {result}.")
    return result


def main():
    test_result = solve("input.test")
    test_answer = 1656
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
