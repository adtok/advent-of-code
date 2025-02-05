"""This one would be fun to optimize"""

from __future__ import annotations

EXAMPLE = "example0.txt"
INPUT = "input.txt"
FILENAME = INPUT

WALL = "#"
EMPTY = "."
START = "S"
END = "E"


Grid = dict[complex, str]
Cheat = tuple[complex, complex]


def main() -> None:
    part_one()
    part_two()


def part_one() -> None:
    track = Track.from_file(FILENAME)
    cheats = track.all_cheats()
    result = sum(timesave >= 100 for _, timesave in cheats)
    print(f"Part one: {result}")


def part_two() -> None:
    track = Track.from_file(FILENAME, cheat_duration=20)
    cheats = track.all_cheats()
    result = sum(timesave >= 100 for _, timesave in cheats)
    print(f"Part two: {result}")


class Track:
    _directions = (-1j, 1, 1j, -1)

    def __init__(
        self, grid: Grid, start: complex, end: complex, cheat_duration: int = 2
    ) -> None:
        self._grid = grid
        for p in list(self._grid):
            for d in Track._directions:
                if p + d not in grid:
                    grid[p + d] = WALL
        self._start = start
        self._end = end
        self._cheat_duration = cheat_duration
        self._path = self.determine_path(grid, start, end)
        print("dists")
        self._dists = {p: {} for p in self.path}
        print(len(self.path))
        for i, p_1 in enumerate(self.path):
            for p_2 in self.path[i:]:
                delta = p_2 - p_1
                dist = int(abs(delta.real) + abs(delta.imag))
                self._dists[p_1][p_2] = dist
                self._dists[p_2][p_1] = dist

        print("done")
        self._time = len(self._path) - 1
        self._cheats: dict[complex, complex] = {}
        self._idx_to_pos = dict(enumerate(self.path))
        self._pos_to_idx = {pos: idx for idx, pos in self._idx_to_pos.items()}
        self._all_cheats: list[Cheat] = None
        print("init done")

    @property
    def grid(self) -> Grid:
        return self._grid

    @property
    def start(self) -> complex:
        return self._start

    @property
    def end(self) -> complex:
        return self._end

    @property
    def path(self) -> list[complex]:
        return self._path

    @property
    def time(self) -> int:
        return self._time

    def cheats(self, pos: complex) -> list[complex]:
        if cached := self._cheats.get(pos):
            return cached
        cheat_ends = (
            e for e in self.path if self._dists[pos][e] <= self._cheat_duration
        )
        result = [e for e in cheat_ends if self.timesave(pos, e) > 0]
        self._cheats[pos] = result
        return result

    def all_cheats(self) -> list[tuple[Cheat, int]]:
        if self._all_cheats:
            return self._all_cheats
        result = []
        for pos in self.path:
            cheats = self.cheats(pos)
            timesaves = (self.timesave(pos, cheat) for cheat in cheats)
            result.extend(zip(((pos, cheat) for cheat in cheats), timesaves))
        return result

    def timesave(self, p_1, p_2) -> int:
        result = self._pos_to_idx[p_2] - self._pos_to_idx[p_1] - self._dists[p_1][p_2]
        return result

    def enhanced_cheats(self, pos: complex) -> list[complex]: ...

    @staticmethod
    def ns(point: complex):
        return (point + d for d in Track._directions)

    @staticmethod
    def distance(p1: complex, p2: complex) -> int:
        result = int(abs(p1.real - p2.real) + abs(p1.imag - p2.imag))
        return result

    @staticmethod
    def determine_path(grid: Grid, start: complex, end: complex) -> list[complex]:
        path = [start]
        ps = (start + d for d in Track._directions)
        ns = (p for p in ps if grid[p] == EMPTY)
        path.append(next(ns))
        while True:
            [prev, curr] = path[-2:]
            if curr == end:
                break
            ps = (curr + d for d in Track._directions)
            ns = (p for p in ps if grid[p] == EMPTY and p != prev)
            path.append(next(ns))
        return path

    @classmethod
    def from_file(cls, filename: str, cheat_duration: int = 2) -> Track:
        grid, start, end = parse(filename)
        return cls(grid=grid, start=start, end=end, cheat_duration=cheat_duration)


def parse(filename: str) -> tuple[Grid, complex, complex]:
    with open(filename, "r") as file:
        grid = {
            complex(col, row): value
            for row, line in enumerate(file)
            for col, value in enumerate(line.strip())
        }
    start = next(coord for coord, value in grid.items() if value == START)
    end = next(coord for coord, value in grid.items() if value == END)
    grid[start] = EMPTY
    grid[end] = EMPTY
    return grid, start, end


def timesave_table(track: Track, min_save: int = 0) -> None:
    timesaves = {}
    for _, ts in track.all_cheats():
        if ts not in timesaves:
            timesaves[ts] = 0
        timesaves[ts] += 1
    ps_width = len(str(max(timesaves)))
    for ps in sorted(timesaves.keys()):
        if ps >= min_save:
            print(f"{ps:{ps_width}} | {timesaves[ps]}")


if __name__ == "__main__":
    main()
