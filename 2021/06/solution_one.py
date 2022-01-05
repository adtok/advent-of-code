"""
Advent of Code 2021: Day 06 part 1
tldr: lanternfish counting/automata simulating kinda
"""

from collections import defaultdict


def solve(input_file: str) -> int:
    school = defaultdict(int)
    with open(input_file, "r") as file:
        for val in map(int, file.read().split(",")):
            school[val] += 1

    for _ in range(80):
        new_school = defaultdict(int)
        for timer, quantity in school.items():
            if timer == 0:
                new_school[8] = quantity
                new_school[6] += quantity
            else:
                new_school[timer - 1] += quantity
        school = new_school

    result = sum(school.values())

    print(f"The answer for {input_file!r} is {result}.")

    return result


def main():
    test_result = solve("input.test")
    test_answer = 5934
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
