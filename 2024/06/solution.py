"""
I am using `complex` type to handle rotations
the delta for going "up" is (-1, 0), because the row index decrements if you're going "up" a row
"""

from typing import TypeAlias

FILENAME = "input.txt"


EMPTY = "."
OBSTACLE = "#"


Pair: TypeAlias = tuple[int, int]
Grid: TypeAlias = dict[Pair, str]


class Guard:
    def __init__(self):
        self._position: Pair = (-1, -1)
        self.start = (-1, -1)
        self._direction: complex = -1j

    def set_starting_position(self, coordinate: Pair) -> None:
        self._position = coordinate
        self.start = coordinate

    @property
    def position(self) -> Pair:
        return self._position

    @property
    def direction(self) -> Pair:
        return (self._direction.imag, self._direction.real)

    @property
    def next_position(self) -> Pair:
        y, x = self.position
        dy, dx = self.direction
        return (y + dy, x + dx)

    @property
    def icon(self):
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

    def turn(self) -> None:
        self._direction *= 1j

    def move(self) -> None:
        self._position = self.next_position


grid = {}
obstacles = {}
seen = set()
direction_log = set()
guard = Guard()
with open(FILENAME, "r") as file:
    for row, line in enumerate(file):
        for col, value in enumerate(line.strip()):
            coordinate = (row, col)
            if value == "^":
                guard.set_starting_position(coordinate)
                grid[coordinate] = "*"
                seen.add(coordinate)
                direction_log.add((guard.position, guard.next_position))
            else:
                grid[coordinate] = value


def print_state(guard: Guard, grid: Grid) -> None:
    width = max(grid, key=lambda c: c[1])[1] + 1
    height = max(grid, key=lambda c: c[0])[0] + 1

    for r in range(width):
        for c in range(height):
            print(grid.get((r, c)) if (r, c) != guard.position else guard.icon, end="")
        print()


print("Starting:")
print_state(guard, grid)

while facing := grid.get(guard.next_position):
    if facing == OBSTACLE:
        guard.turn()
    else:
        guard.move()
        seen.add(guard.position)
        direction_log.add((guard.position, guard.next_position))
    # print_state(guard, grid)

print(f"Part 1 {len(seen)} {len(direction_log)}")


def would_loop(log_entry: tuple[Pair, Pair], grid: Grid) -> bool:
    width = max(grid, key=lambda c: c[1])[1] + 1
    height = max(grid, key=lambda c: c[0])[0] + 1
    pos, next_pos = log_entry
    if grid.get(next_pos, "*") != "*":
        return False
