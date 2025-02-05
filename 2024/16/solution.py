from __future__ import annotations

import heapq
from collections import defaultdict, deque

EXAMPLE_0 = "example0.txt"
EXAMPLE_1 = "example1.txt"
INPUT = "input.txt"
FILENAME = INPUT

WALL = "#"
EMPTY = "."
START = "S"
END = "E"

STARTING_DIRECTION = complex(1, 0)

COST_MOVE = 1
COST_TURN = 1000

State = tuple[complex, complex]


def main() -> None:
    part_one()
    print()
    part_two()


def part_one() -> None:
    for filename in [EXAMPLE_0, EXAMPLE_1]:
        maze = Maze.from_file(filename)
        result, _ = solve(maze)
        print(f"{filename}: {result}")
        print()
    maze = Maze.from_file(FILENAME)
    result, _ = solve(maze)
    print(f"Part one: {result}")


def part_two() -> None:
    for filename in [EXAMPLE_0, EXAMPLE_1]:
        maze = Maze.from_file(filename)
        _, result = solve(maze)
        print(f"{filename}: {result}")
        print()
    maze = Maze.from_file(FILENAME)
    _, result = solve(maze)
    print(f"Part two: {result}")


def solve(maze: Maze) -> tuple[int, int]:
    beginning_state = (maze.start, STARTING_DIRECTION)
    seen = []
    best = 1e9
    costs = defaultdict(lambda: 1e9)

    queue = [(0, t := 0, maze.start, 1, [maze.start])]
    while queue:
        cost, _, pos, direction, path = heapq.heappop(queue)
        if cost > costs[(pos, direction)]:
            continue
        costs[(pos, direction)] = cost

        if pos == maze.end and cost <= best:
            seen += path
            best = cost

        for rotation, cost_m in (1, 1), (1j, 1001), (-1j, 1001):
            cost_new = cost + cost_m
            t += 1
            pos_new = pos + direction * rotation
            dir_new = direction * rotation
            if pos_new not in maze.grid or maze.grid[pos_new] == WALL:
                continue
            heapq.heappush(queue, (cost_new, t, pos_new, dir_new, path + [pos_new]))

    result = best, len(set(seen))
    return result


def solvex(maze: Maze) -> int:
    beginning_state = (maze.start, STARTING_DIRECTION)
    costs: dict[State, int] = {beginning_state: 0}
    queue = deque([beginning_state])

    def search(state: State, cost: int) -> None:
        ms_and_cs = maze.move_costs(state)
        for state_m, cost_m in ms_and_cs:
            if state_m[0] == maze.end:
                print("x", state, state_m, cost_m)
            if state_m not in costs or costs[state_m] > cost + cost_m:
                queue.append(state_m)
                costs[state_m] = cost + cost_m

    while queue:
        state = queue.popleft()
        cost = costs[state]
        if state[0] == maze.end:
            print(cost)
        # print(state, cost, queue)
        # input()
        search(state, cost)

    end_costs = [cost for (pos, _), cost in costs.items() if pos == maze.end]
    print(end_costs)

    print(maze.end in (pos for pos, _ in costs))


class Maze:
    def __init__(self, grid: dict[complex, str], start: complex, end: complex) -> None:
        self._grid = grid
        self._start = start
        self._end = end

    @property
    def grid(self) -> dict[complex, str]:
        return self._grid

    @property
    def start(self) -> complex:
        return self._start

    @property
    def end(self) -> complex:
        return self._end

    def move_costs(self, state: State) -> list[tuple[State, int]]:
        position, direction = state
        turns_and_costs = (
            (direction, 0),
            (direction * 1j, 1),
            (direction * -1, 2),
            (direction * -1j, 1),
        )
        # turns_and_costs = ((direction * (1j**i), i) for i in range(4))
        result = [
            ((position + new_direction, new_direction), COST_MOVE + (COST_TURN * turns))
            for new_direction, turns in turns_and_costs
            if self.grid[position + new_direction] != WALL
        ]
        # print(state, result)
        return result

    @classmethod
    def from_file(cls, filename) -> Maze:
        grid, start, end = parse(filename)
        return cls(grid=grid, start=start, end=end)


def parse(filename: str) -> tuple[dict[complex, str], complex, complex]:
    with open(filename, "r") as file:
        grid = {
            complex(col, row): value
            for row, line in enumerate(file)
            for col, value in enumerate(line.strip())
        }
    start = [coord for coord, value in grid.items() if value == START][0]
    end = [coord for coord, value in grid.items() if value == END][0]
    grid[start] = EMPTY
    grid[end] = EMPTY
    return grid, start, end


if __name__ == "__main__":
    main()
    # print(n_turns(UP, RIGHT))
    # print(n_turns(UP, DOWN))
    # print(n_turns(UP, LEFT))
    # print(n_turns(UP, UP))
    # print(n_turns(RIGHT, DOWN))
    # print(n_turns(RIGHT, LEFT))
    # print(n_turns(RIGHT, UP))
    # print(n_turns(RIGHT, RIGHT))
    # print(n_turns(DOWN, LEFT))
    # print(n_turns(DOWN, UP))
    # print(n_turns(DOWN, RIGHT))
    # print(n_turns(DOWN, DOWN))
    # print(n_turns(LEFT, UP))
    # print(n_turns(LEFT, RIGHT))
    # print(n_turns(LEFT, DOWN))
    # print(n_turns(LEFT, LEFT))
