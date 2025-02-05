FILENAME = "example.txt"

EXAMPLE_ONE = "0 1 10 99 999"
EXAMPLE_TWO = "125 17"
INPUT = "965842 9159 3372473 311 0 6 86213 48"


def main():
    part_one()
    part_two()
    experiment()


def part_one():
    start = parse(INPUT)
    end = simulate(start, 25)
    result = len(end)
    print(f"Part one: {result}")


def part_two():
    start = parse_map(INPUT)
    end = simulate_map(start, 75)
    result = sum(end.values())
    print(f"Part two: {result}")


def experiment():
    start = parse(INPUT)
    end = map(lambda x: simulate([x], 75), start)
    result = sum(map(sum, end))
    print(f"Experiment: {result}")


def parse(line: str) -> list[int]:
    return list(map(int, line.split()))


def parse_map(line: str) -> list[int]:
    stones = parse(line)
    result = {stone: stones.count(stone) for stone in stones}
    return result


def split_even(stone: int) -> list[int]:
    string = str(stone)
    length = len(string)
    return [int(string[: length // 2]), int(string[length // 2 :])]


def change(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    string = str(stone)
    length = len(string)
    if length % 2 == 0:
        return split_even(stone)
    return [stone * 2024]


def blink(stones: list[int]) -> list[int]:
    result = []
    for changed in map(change, stones):
        result.extend(changed)
    return result


def blink_map(stones: dict[int, int]) -> dict[int, int]:
    result = {}
    for stone, count in stones.items():
        new = change(stone)
        for value in new:
            if value not in result:
                result[value] = 0
            result[value] += count
    return result


def simulate(stones: list[int], times: int) -> list[int]:
    if times == 0:
        return stones
    return simulate(blink(stones), times - 1)


def simulate_map(stones: dict[int, int], times: int) -> dict[int, int]:
    if times == 0:
        return stones
    return simulate_map(blink_map(stones), times - 1)


if __name__ == "__main__":
    main()
