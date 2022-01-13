"""Advent of Code 2015: Day 16"""

from typing import Callable, Dict, Generator


# Reading data given from the AoC website
READING = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def parse_sue(line: str) -> Dict[str, int]:
    """Takes a line of input data and gets the Sue's number and the data you remember"""
    _, num, *data = line.replace(":", "").replace(",", "").split()
    num = int(num)
    data = dict(zip(data[::2], map(int, data[1::2])))
    return num, data


def iterate_sues(input_file: str) -> Generator:
    """Iterates through all the sues in the file"""
    with open(input_file, "r") as file:
        yield from map(parse_sue, file)


def part_one(input_file: str) -> int:
    for num, sue in iterate_sues(input_file):

        def check(key):
            return READING[key] == sue[key]

        if all(map(check, sue)):
            return num
    return -1


def part_two(input_file: str) -> int:
    for num, sue in iterate_sues(input_file):

        def check(key):
            if key in {"cats", "trees"}:
                return sue[key] > READING[key]
            elif key in {"pomeranians", "goldfish"}:
                return sue[key] < READING[key]
            else:
                return sue[key] == READING[key]

        if all(map(check, sue)):
            return num

    return -1


def solve(func: Callable[[str], int]):
    input_file = "data/16.solution"
    result = func(input_file)
    print(f"The solution for {func.__name__!r} is {result}")


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
