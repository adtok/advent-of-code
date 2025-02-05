from __future__ import annotations

import functools
import time
from typing import Generator

FILENAME = "example.txt"

DIRECTIONS = [NORTH, EAST, SOUTH, WEST] = [(-1, 0), (0, 1), (1, 0), (0, -1)]
TRAILHEAD = 0
TERMINAL = 9

Point = tuple[int, int]
Grid = dict[Point, int]


def timed(fn):
    def _fn():
        start = time.perf_counter()
        fn()
        end = time.perf_counter()
        print(f"\ttook {end - start:.6f} seconds")

    return _fn


def main() -> None:
    part_one()
    print("##########")
    part_two()
    print("##########")
    part_one_slow()
    print("##########")
    part_two_slow()


@timed
def part_one() -> None:
    """The score of a trailhead is the number of unique '9' heights it can reach"""
    heightmap = Heightmap.from_file(FILENAME)
    result = sum(len(heightmap.score(trailhead)) for trailhead in heightmap.trailheads)
    print(f"Part one: {result}")


@timed
def part_two() -> None:
    """The rating of a trailhead is the number its unique hiking paths"""
    heightmap = Heightmap.from_file(FILENAME)
    result = sum(heightmap.rating(trailhead) for trailhead in heightmap.trailheads)
    print(f"Part two: {result}")


@timed
def part_one_slow() -> None:
    """The score of a trailhead is the number of unique '9' heights it can reach"""
    heightmap = Heightmap.from_file(FILENAME)
    result = sum(
        Heightmap.score_slow(trailhead, heightmap) for trailhead in heightmap.trailheads
    )
    print(f"Part one: {result} (slow)")


@timed
def part_two_slow() -> None:
    """The score of a trailhead is the number of unique '9' heights it can reach"""
    heightmap = Heightmap.from_file(FILENAME)
    result = sum(
        Heightmap.rating_slow(trailhead, heightmap)
        for trailhead in heightmap.trailheads
    )
    print(f"Part two: {result} (slow)")


class Heightmap(dict):
    def __init__(self, grid: Grid) -> None:
        for key, value in grid.items():
            self[key] = value
        self._height = max(grid, key=lambda x: x[0])[0]
        self._width = max(grid, key=lambda x: x[1])[1]
        self._trailheads = [
            (row, col) for (row, col), value in self.items() if value == TRAILHEAD
        ]
        self._terminals = [
            (row, col) for (row, col), value in self.items() if value == TERMINAL
        ]
        self._scores: dict[Point, set[Point]] = {}
        self._ratings: Grid = {}

    @classmethod
    def from_file(cls, filename: str) -> Heightmap:
        with open(filename, "r") as file:
            grid = {
                (row, col): int(height)
                for row, line in enumerate(file)
                for col, height in enumerate(line.strip())
            }
        return cls(grid=grid)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def trailheads(self) -> list[Point]:
        return self._trailheads

    @property
    def terminals(self) -> list[Point]:
        return self._terminals

    def neighbors(self, coord: Point) -> Generator[Point, None, None]:
        y, x = coord
        points = ((y + dy, x + dx) for dy, dx in DIRECTIONS)
        return (point for point in points if point in self)

    def moves(self, coord: Point) -> Generator[Point, None, None]:
        return (
            neighbor
            for neighbor in self.neighbors(coord)
            if self[neighbor] == self[coord] + 1
        )

    def score(self, point: Point) -> int:
        assert point in self, f"{point} not in heightmap"
        if (terminals := self._scores.get(point)) is not None:
            return terminals
        if self[point] == TERMINAL:
            self._scores[point] = {point}
            return {point}
        result = functools.reduce(
            lambda x, y: x | y, (self.score(move) for move in self.moves(point)), set()
        )
        self._scores[point] = result
        return result

    def _explore(self, point: Point) -> int:
        assert point in self, f"{point} not in heightmap"
        if (rating := self._ratings.get(point)) is not None:
            return rating
        if self[point] == TERMINAL:
            self._ratings[point] = 1
            return 1
        result = sum(self._explore(move) for move in self.moves(point))
        self._ratings[point] = result
        return result

    def rating(self, trailhead: Point) -> int:
        assert self[trailhead] == TRAILHEAD, f"{trailhead} is not a trailhead"

        result = self._explore(trailhead)

        return result

    @staticmethod
    def score_slow(trailhead: Point, heightmap: Heightmap) -> int:
        assert heightmap[trailhead] == TRAILHEAD, f"{trailhead} is not a trailhead"
        stack = [trailhead]
        seen = set()
        terminals = 0
        while stack:
            coordinate = stack.pop()
            if coordinate in seen:
                continue
            seen.add(coordinate)
            if heightmap[coordinate] == TERMINAL:
                terminals += 1
            stack.extend(heightmap.moves(coordinate))
        return terminals

    @staticmethod
    def rating_slow(trailhead: Point, heightmap: Heightmap) -> int:
        assert heightmap[trailhead] == TRAILHEAD, f"{trailhead} is not a trailhead"

        def explore(coord: Point) -> bool:
            if heightmap[coord] == TERMINAL:
                return 1
            result = sum(explore(move) for move in heightmap.moves(coord))
            return result

        return explore(trailhead)


@timed
def experiment():
    heightmap = Heightmap.from_file("example2.txt")
    graph = {source: {dest: 0 for dest in heightmap} for source in heightmap}
    for point in heightmap:
        subgraph = graph[point]
        stack = [point]
        while stack:
            curr = stack.pop()
            subgraph[curr] = 1
            # print([move for move in heightmap.moves(curr) if not subgraph[move]])
            stack.extend(move for move in heightmap.moves(curr) if not subgraph[move])
            # print(stack)
        # print(point, subgraph)


if __name__ == "__main__":
    main()
    # experiment()
