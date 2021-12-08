"""
Advent of Code 2021: Day 07 Part 1
tldr: count the occurences of certain digits
"""


from typing import List, Tuple


def parse_line(line: str) -> Tuple[List[str], List[str]]:
    patterns, output = line.strip().split(" | ")
    patterns = patterns.split(" ")
    output = output.split(" ")
    return patterns, output


def is_unique(digit: str) -> bool:
    """Returns if a digit can be deduced solely by the length of its representation"""
    return len(digit) in {2, 3, 4, 7}


def solve(input_file: str) -> int:
    with open(input_file, "r") as file:
        result = sum(sum(map(is_unique, output)) for _, output in map(parse_line, file))

    print(f"The solution for {input_file!r} is {result}.")

    return result


def main():
    test_result = solve("input.test")
    test_answer = 26
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
