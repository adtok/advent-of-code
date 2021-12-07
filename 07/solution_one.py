"""
Advent of Code 2021: Day 07 part 1
tldr: cost to move
"""


def solve(input_file: str) -> int:
    with open(input_file, "r") as file:
        crabs = list(map(int, file.read().split(",")))

    lo, hi = min(crabs), max(crabs)

    fuel_costs = [
        sum(map(lambda crab: abs(crab - pos), crabs)) for pos in range(lo, hi + 1)
    ]

    result = min(fuel_costs)

    print(f"The answer for {input_file!r} is {result}.")

    return result


def main():
    test_result = solve("input.test")
    test_answer = 37
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
