"""Advent of Code 2015: Day 18"""


from dataclasses import dataclass
from typing import Callable, List


DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


@dataclass
class Grid:
    lights: List[List[int]]
    rows: int = 100
    cols: int = 100

    @property
    def lights_on(self):
        return sum(sum(row) for row in self.lights)

    def neighbors(self, row, col):
        for dr, dc in DIRS:
            nr = row + dr
            nc = col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                yield (nr, nc)

    def four_corners_on(self):
        mr = self.rows - 1
        mc = self.cols - 1
        for row, col in ((0, 0), (mr, 0), (0, mc), (mr, mc)):
            self.lights[row][col] = 1

    def next_state(self, row, col):
        light = self.lights[row][col]
        neighbors_on = sum(self.lights[r][c] for r, c in self.neighbors(row, col))
        if light == 1:
            if neighbors_on not in {2, 3}:
                return 0
            else:
                return 1
        elif light == 0:
            if neighbors_on == 3:
                return 1
            else:
                return 0
        raise Exception("Something went wrong")

    def iterate(self):
        new_lights = [
            [self.next_state(row, col) for col in range(self.cols)]
            for row in range(self.rows)
        ]
        self.lights = new_lights

    @classmethod
    def from_file(cls, input_file: str):
        with open(input_file, "r") as file:
            data = [[int(c == "#") for c in line.strip()] for line in file]
        rows = len(data)
        cols = len(data[0])
        return cls(lights=data, rows=rows, cols=cols)


def part_one(input_file: str) -> int:
    grid = Grid.from_file(input_file)
    for _ in range(100):
        grid.iterate()
    result = grid.lights_on
    return result


def part_two(input_file: str) -> int:
    grid = Grid.from_file(input_file)
    grid.four_corners_on()
    for _ in range(100):
        grid.iterate()
        grid.four_corners_on()
    result = grid.lights_on
    return result


def solve(func: Callable[[str], int]):
    input_file = "data/18.solution"
    result = func(input_file)
    print(f"The solution for {func.__name__!r} is {result}")


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
