"""
Advemt of Code 2021: Day 15 Part 1
tldr: lowest cost path
"""


from typing import List, Tuple


DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def in_bounds(x: int, y: int, w: int, h: int) -> bool:
    return 0 <= x < w and 0 <= y < h


def get_neighbors(x: int, y: int, w: int, h: int) -> List[Tuple[int, int]]:
    tmp = [(x + dx, y + dy) for dx, dy in DIRS]
    return [(px, py) for px, py in tmp if in_bounds(px, py, w, h)]


def solve(input_file: str) -> int:
    with open(input_file, "r") as file:
        riskmap = [list(map(int, line.strip())) for line in file.readlines()]

    h = len(riskmap)
    w = len(riskmap[0])
    pos = (0, 0)

    cost = [[float("inf") for _ in range(w)] for _ in range(h)]

    cost[0][0] = 0

    queue = [pos]

    while queue:
        current = queue.pop(0)
        cx, cy = current
        cost_c = cost[cy][cx]
        for nx, ny in get_neighbors(cx, cy, w, h):
            cost_n = cost[ny][nx]
            risk_n = riskmap[ny][nx]
            cost_to_neighbor = cost_c + risk_n
            if cost_to_neighbor < cost_n:
                cost[ny][nx] = cost_to_neighbor
                queue.append((nx, ny))

    result = cost[h - 1][w - 1]

    print(f"The solution to {input_file!r} is {result}.")

    return result


def main():
    test_result = solve("input.test")
    test_answer = 40
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
