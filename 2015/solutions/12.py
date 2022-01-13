import json
from typing import Callable, List


def sum_json(obj):
    if isinstance(obj, dict):
        return sum_json(list(obj.values()))
    elif isinstance(obj, list):
        return sum(sum_json(item) for item in obj)
    elif isinstance(obj, int):
        return obj
    return 0


def sum_json_ignore(obj, ignore_value):
    if isinstance(obj, dict):
        if ignore_value in list(obj.values()):
            return 0
        return sum_json_ignore(list(obj.values()), ignore_value)
    elif isinstance(obj, list):
        return sum(sum_json_ignore(item, ignore_value) for item in obj)
    elif isinstance(obj, int):
        return obj
    return 0


def solve(func: Callable[[str], int]):
    input_value = "data/12.solution"
    result = func(input_value)
    print(f"The solution for {func.__name__!r} is {result}")


def part_one(input_file: str) -> int:
    with open(input_file, "r") as file:
        data = json.load(file)
    result = sum_json(data)
    return result


def part_two(input_file: str) -> int:
    with open(input_file, "r") as file:
        data = json.load(file)
    result = sum_json_ignore(data, "red")
    return result


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
