"""
I am using `complex` type to handle rotations
the delta for going "up" is (-1, 0), because the row index decrements if you're going "up" a row
"""

from __future__ import annotations

from typing import TypeAlias

FILENAME = "example.txt"


EMPTY = "."
OBSTACLE = "#"


Pair: TypeAlias = tuple[int, int]
Grid: TypeAlias = dict[Pair, str]


def main():
    game = Game.from_file(FILENAME)
    game.simulate()


def _complex_to_vec2(c: complex) -> Vec2:
    return (c.imag, c.real)


class Game:
    def __init__(self, position: Pair, grid: Grid) -> None:
        # guard
        self._position = position
        self._direction: complex = -1j

        # grid
        self._grid = grid
        self._width = max(grid, key=lambda c: c[1])[1] + 1
        self._height = max(grid, key=lambda c: c[0])[0] + 1

        # logs
        self._seen: set[Pair] = {position}
        self._logs: set[tuple[Pair, Pair]] = {(position, (-1, 0))}

    @classmethod
    def from_file(cls, filename: str) -> Game:
        grid = {}
        starting_position = None
        with open(filename, "r") as file:
            for row, line in enumerate(file):
                for col, value in enumerate(line.strip()):
                    coordinate = (row, col)
                    if value == "^":
                        starting_position = (row, col)
                        grid[coordinate] = "*"
                    else:
                        grid[coordinate] = value
        return cls(position=starting_position, grid=grid)

    @property
    def position(self) -> Pair:
        return self._position

    @property
    def direction(self) -> Pair:
        return _complex_to_vec2(self._direction)

    @property
    def next_position(self) -> Pair:
        y, x = self.position
        dy, dx = self.direction
        return (y + dy, x + dx)

    @property
    def guard_icon(self):
        if self.direction == (-1, 0):
            return "^"
        elif self.direction == (0, 1):
            return ">"
        elif self.direction == (1, 0):
            return "v"
        elif self.direction == (0, -1):
            return "<"
        else:
            raise ValueError(f"{self.direction=}")

    def _see(self) -> None:
        self._seen.add(self.position)

    def _log(self) -> None:
        self._seen.add(self.position)
        self._logs.add((self.position, self.direction))

    def _turn(self) -> None:
        self._direction *= 1j
        self._log()

    def _move(self) -> None:
        self._position = self.next_position
        self._see()
        self._log()

    def simulate(self) -> None:
        while facing := self._grid.get(self.direction):
            if facing == OBSTACLE:
                self._turn()
            else:
                self._move()
            # print_state(guard, grid)

        print(f"Part 1 {len(self._seen)} {len(self._logs)}")


if __name__ == "__main__":
    main()
