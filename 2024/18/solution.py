from collections import deque

EXAMPLE = "example0.txt"
INPUT = "input.txt"
FILENAME = INPUT

SIZE = (WIDTH, HEIGHT) = (71, 71) if FILENAME == INPUT else (7, 7)
END = (WIDTH - 1, HEIGHT - 1)

P1_TAKE = 1024 if FILENAME == INPUT else 12


Point = tuple[int, int]


def main() -> None:
    part_one()
    part_two()


def part_one() -> None:
    bs = parse(FILENAME)
    costs = calculate_costs(bs, P1_TAKE)
    result = costs.get(END)
    print(f"Part one: {result}")


def part_two() -> None:
    bs = parse(FILENAME)
    result = first_blocked(bs)
    print(f"Part two: {result}")


def parse(filename: str) -> list[Point]:
    with open(filename, "r") as file:
        result = [tuple(map(int, line.split(","))) for line in file]
    return result


def calculate_costs(bs: list[Point], take: int) -> dict[Point, int]:
    start = (0, 0)
    costs = {start: 0}
    queue = deque([start])
    blocks = set(bs[:take])

    def search(point: Point, c: int) -> None:
        ns = neighbors(point)
        for p in ns:
            if p not in blocks and (p not in costs or costs[p] > c):
                queue.append(p)
                costs[p] = c

    while queue:
        pos = queue.pop()
        cost = costs[pos]
        search(pos, cost + 1)

    return costs


def first_blocked(bs: list[Point]) -> Point | None:
    costs = calculate_costs(bs, P1_TAKE)
    path = set(shortest_path(costs))
    i = P1_TAKE
    for i in range(P1_TAKE, len(bs)):
        if bs[i] not in path:
            continue
        costs = calculate_costs(bs, i + 1)
        if END not in costs:
            return bs[i]
        path = set(shortest_path(costs))
    return None


def shortest_path(costs: dict[Point, int]) -> list[Point]:
    pos = END
    path = deque([pos])
    while pos != (0, 0):
        cost = costs[pos]
        ns = [n for n in neighbors(pos) if costs.get(n, -1) == cost - 1]
        pos = min(ns, key=lambda n: costs[n])
        path.appendleft(pos)
    return path


def can_reach(bs: list[Point], take: int) -> bool:
    blocks = set(bs[:take])
    start = (0, 0)
    seen = {start}
    queue = deque([start])
    while queue:
        pos = queue.popleft()
        ns = neighbors(pos)
        to_visit = set(ns) - (blocks | seen)
        queue.extend(to_visit)
        seen |= to_visit
        # print(f"{pos} {queue} {ns} {blocks | seen}")
        # input()
    result = END in seen
    return result


_directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def neighbors(p: Point) -> list[Point]:
    x, y = p
    points = ((x + dx, y + dy) for dx, dy in _directions)
    valid = ((x, y) for x, y in points if 0 <= x < WIDTH and 0 <= y < HEIGHT)
    result = list(valid)
    return result


if __name__ == "__main__":
    main()
