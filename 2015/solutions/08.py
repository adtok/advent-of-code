"""Advent of Code 2015: Day 8"""


from typing import Callable


def iterate_file(input_file: str):
    with open(input_file, "r") as file:
        for line in file:
            yield line.strip()


def in_memory_size(string: str) -> int:
    count = 0
    i = 0
    while i < len(string):
        if string[i] == "\\":
            i += 1
            if string[i] == "x":
                i += 2
        count += 1
        i += 1
    result = count - 2
    return result


def encode_string(string: str) -> int:
    new_string = ""
    for i, char in enumerate(string):
        if char == '"':
            new_string += '\\"'
        elif char == "\\":
            new_string += "\\\\"
        else:
            new_string += char

    result = f'"{new_string}"'
    return result


def part_one(input_file: str):
    calc = lambda s: len(s) - in_memory_size(s)
    result = sum(map(calc, iterate_file(input_file)))
    return result


def part_two(input_file: str):
    calc = lambda s: len(encode_string(s)) - len(s)
    result = sum(map(calc, iterate_file(input_file)))
    return result


def solve(func: Callable[[str], int]):
    input_file = "data/08.solution"
    result = func(input_file)
    print(f"The solution for {func.__name__!r} is {result}")


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
