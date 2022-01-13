"""
Advent of Code 2015: Day 5
"""


from typing import Callable


VOWELS = "aeoiu"
BAD_PAIRS = ["ab", "cd", "pq", "xy"]


def bad_pairs(string: str) -> bool:
    return any(bad_pair in string for bad_pair in BAD_PAIRS)


def count_vowels(string: str) -> int:
    return sum(string.count(vowel) for vowel in VOWELS)


def has_couple(string: str) -> bool:
    for i, char in enumerate(string):
        if i > 0 and string[i - 1] == char:
            return True
    return False


def has_double_pair(string: str) -> bool:
    for a, b in zip(string, string[1:]):
        if string.count(a + b) > 1:
            return True
    return False


def has_offset_repeat(string: str) -> bool:
    for i, char in enumerate(string):
        if i > 1 and string[i - 2] == char:
            return True
    return False


def part_one(string: str) -> bool:
    has_bad_pair = bad_pairs(string)
    vowels = count_vowels(string)
    couple_found = has_couple(string)
    return vowels >= 3 and couple_found and not has_bad_pair


def part_two(string: str) -> bool:
    double_pair = has_double_pair(string)
    offset_repeat = has_offset_repeat(string)
    return double_pair and offset_repeat


def solve(input_file: str, nice_string_function: Callable) -> int:
    with open(input_file, "r") as file:
        result = sum(map(nice_string_function, map(str.strip, file)))
    print(f"The solution using {nice_string_function.__name__!r} is {result}")


def main():
    solve("data/05.solution", part_one)
    solve("data/05.solution", part_two)


if __name__ == "__main__":
    main()
