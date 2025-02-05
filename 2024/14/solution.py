EXAMPLE = "example.txt"
INPUT = "input.txt"
FILENAME = INPUT
EXAMPLE_SIZE = (11, 7)
INPUT_SIZE = (101, 103)
SIZE = (WIDTH, HEIGHT) = INPUT_SIZE if FILENAME == INPUT else EXAMPLE_SIZE
MID_X = WIDTH // 2
MID_Y = HEIGHT // 2
TIMESTEPS = 100

Robot = tuple[int, int, int, int]
Vec2 = tuple[int, int]


def main() -> None:
    part_one()
    part_two()


def part_one() -> None:
    quadrants = {q: 0 for q in (1, 2, 3, 4)}
    with open(FILENAME, "r") as file:
        for line in file:
            robot = parse(line)
            x, y = simulate(robot, TIMESTEPS)
            if q := quadrant(x, y):
                quadrants[q] += 1
    result = quadrants[1] * quadrants[2] * quadrants[3] * quadrants[4]
    print(f"Part 1: {result}")


def part_two() -> None:
    with open(FILENAME, "r") as file:
        robots = list(map(parse, file))

    ps = [(x, y) for x, y, *_ in robots]
    pxs = [[p[0] for p in ps]]
    pys = [[p[1] for p in ps]]
    vs = [(x, y) for *_, x, y in robots]
    vxs = [v[0] for v in vs]
    vys = [v[1] for v in vs]

    safety_factors = [safety_factor(ps)]
    all_ps = [ps]
    curr = ps
    for _ in range(10_000):
        new = [
            ((px + vx) % WIDTH, (py + vy) % HEIGHT)
            for (px, py), (vx, vy) in zip(curr, vs)
        ]
        all_ps.append(new)
        safety_factors.append(safety_factor(new))
        curr = new

    lowest_safety = min(list(zip(all_ps, safety_factors)), key=lambda z: z[1])[1]
    result = safety_factors.index(lowest_safety)
    show(all_ps[result])
    print(f"Part 1: {result}")

    # i = 0
    # while i := i + 1:
    #     ps = [(px + vx, py + vy) for (px, py), (vx, vy) in zip(ps, vs)]
    #     if len(ps) == len(set(ps)):
    #         break
    # result = i

    # # pxv = [variance(pxs[0])]
    # # pyv = [variance(pys[0])]
    # # for _ in range(WIDTH):
    # #     xs = [p + v for p, v in zip(pxs[-1], vxs)]
    # #     var_xs = variance(xs)
    # #     pxs.append(xs)
    # #     pxv.append(var_xs)
    # # for _ in range(HEIGHT):
    # #     ys = [p + v for p, v in zip(pys[-1], vys)]
    # #     var_ys = variance(ys)
    # #     pys.append(ys)
    # #     pyv.append(var_ys)
    # # print(pxv, pyv, sep="\n")

    # # best_xs_index = min(list(enumerate(pxv)), key=lambda p: p[1])[0]
    # # best_ys_index = min(list(enumerate(pyv)), key=lambda p: p[1])[0]

    # # best = list(zip(pxs[best_xs_index], pys[best_ys_index]))

    # # show(best)

    # # result = None


def parse(line: str) -> Robot:
    [pos_str, vel_str] = line.split(" ")
    [px, py] = pos_str[2:].split(",")
    [vx, vy] = vel_str[2:].split(",")
    result = (int(px), int(py), int(vx), int(vy))
    return result


def simulate(robot: Robot, dt: int) -> tuple[int, int]:
    px, py, vx, vy = robot
    x_ = (px + vx * dt) % WIDTH
    y_ = (py + vy * dt) % HEIGHT
    result = (x_, y_)
    return result


def quadrant(x: int, y: int) -> int | None:
    if x == MID_X or y == MID_Y:
        return None
    if x < MID_X and y < MID_Y:
        return 1
    if x > MID_X and y < MID_Y:
        return 2
    if x < MID_X and y > MID_Y:
        return 3
    if x > MID_X and y > MID_Y:
        return 4


def show(robots: list[Vec2]) -> None:
    rs = set()
    for x, y in robots:
        rs.add((x, y))
    for row in range(HEIGHT):
        for col in range(WIDTH):
            print("*" if (col, row) in rs else ".", end="")
        print()


def safety_factor(robots: list[Vec2]) -> int:
    quadrants = {q: 0 for q in (1, 2, 3, 4)}
    for x, y in robots:
        if q := quadrant(x, y):
            quadrants[q] += 1
    result = quadrants[1] * quadrants[2] * quadrants[3] * quadrants[4]
    return result


def variance(xs: list[int]) -> float:
    n = len(xs)
    mean = sum(xs) / n
    differences = (x - mean for x in xs)
    result = sum(diff**2 for diff in differences) / n
    return result


if __name__ == "__main__":
    main()
