"""
I am using `complex` type to handle rotations
the delta for going "up" is (-1, 0), because the row index decrements if you're going "up" a row
"""

from __future__ import annotations

from typing import TypeAlias

FILENAME = "input.txt"


EMPTY = "."
OBSTACLE = "#"


Vec2: TypeAlias = tuple[int, int]
Grid: TypeAlias = dict[Vec2, str]
Velocity: TypeAlias = tuple[Vec2, Vec2]


def main():
    game = Game.from_file(FILENAME)
    game.simulate()
    game.part_one()

    game.part_two()


def _complex_to_vec2(c: complex) -> Vec2:
    return (c.imag, c.real)


class Game:
    def __init__(
        self, position: Vec2, grid: Grid, initial_direction: complex = -1j
    ) -> None:
        # guard
        self._position = position
        self._direction: complex = initial_direction

        # grid
        self._grid = grid
        self._width = max(grid, key=lambda c: c[1])[1] + 1
        self._height = max(grid, key=lambda c: c[0])[0] + 1

        # logs
        self._seen: set[Vec2] = {position}
        self._logs: set[tuple[Vec2, Vec2]] = {(position, (-1, 0))}

        # loops
        self._simulation_result = None
        self._starting_position = position
        self._pos_dir_loops: dict[Vec2, bool] = {}

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

    @classmethod
    def _would_loop(cls, grid: Grid, starting_position: Vec2) -> bool:
        game = cls(position=starting_position, grid=grid)
        result = game.simulate()
        return result

    @property
    def position(self) -> Vec2:
        return self._position

    @property
    def direction(self) -> Vec2:
        return _complex_to_vec2(self._direction)

    @property
    def next_position(self) -> Vec2:
        y, x = self.position
        dy, dx = self.direction
        return (y + dy, x + dx)

    @property
    def _velocity(self) -> Velocity:
        return (self.position, self.direction)

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

    def simulate(self) -> bool:
        """Returns whether the simulation has a loop"""
        if self._simulation_result is not None:
            return self._simulation_result
        while facing := self._grid.get(self.next_position):
            if facing == OBSTACLE:
                self._turn()
            else:
                # If we have had a specific velocity before, it means there is a loop
                if (self.next_position, self.direction) in self._logs:
                    self._simulation_result = True
                    return True
                self._move()

        self._simulation_result = False
        return False

    def part_one(self) -> None:

        print(f"Part 1 {len(self._seen)} {len(self._logs)}")

    def part_two(self) -> None:
        for velocity in self._logs:
            self._find_loop(velocity)
        print(sum(self._pos_dir_loops.values()))

    def _find_loop_(self, velocity: Velocity) -> bool:
        ((y, x), (dy, dx)) = velocity
        next_position = (y + dy, x + dx)
        if next_position not in self._grid or next_position in self._pos_dir_loops:
            return
        new_grid = dict(self._grid.items())
        new_grid[next_position] = OBSTACLE
        result = self._would_loop(new_grid, self._starting_position)
        self._pos_dir_loops[next_position] = result

    def print_state(self) -> None:
        for r in range(self._width):
            for c in range(self._height):
                print(
                    (
                        self._grid.get((r, c))
                        if (r, c) != self._position
                        else self.guard_icon
                    ),
                    end="",
                )
            print()


if __name__ == "__main__":
    main()
