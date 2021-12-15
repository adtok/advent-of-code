"""
Advemt of Code 2021: Day 15 Part 1
tldr: lowest cost path but way bigger
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

    original_h = len(riskmap)
    original_w = len(riskmap[0])
    h = original_h * 5
    w = original_w * 5
    pos = (0, 0)

    riskmap_big = [[None for _ in range(w)] for _ in range(h)]

    def get_risk(point: Tuple[int, int]) -> int:
        px, py = point
        if riskmap_big[py][px] is not None:
            return riskmap_big[py][px]

        x_offset = px // original_w
        ox = px % original_w
        y_offset = py // original_h
        oy = py % original_h

        risk_o = riskmap[oy][ox]
        risk_m = risk_o + x_offset + y_offset
        risk = (risk_m - 1) % 9 + 1

        riskmap_big[py][px] = risk

        return risk

    cost = [[float("inf") for _ in range(w)] for _ in range(h)]

    cost[0][0] = 0

    queue = [pos]

    while queue:
        current = queue.pop(0)
        cx, cy = current
        cost_c = cost[cy][cx]
        for nx, ny in get_neighbors(cx, cy, w, h):
            cost_n = cost[ny][nx]
            risk_n = get_risk((nx, ny))
            cost_to_neighbor = cost_c + risk_n
            if cost_to_neighbor < cost_n:
                cost[ny][nx] = cost_to_neighbor
                queue.append((nx, ny))

    result = cost[h - 1][w - 1]

    print(f"The solution to {input_file!r} is {result}.")

    return result


def main():
    test_result = solve("input.test")
    test_answer = 315
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
