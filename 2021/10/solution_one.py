"""
Advent of Code 2021: Day 10 Part 1
tldr: first invalid parenthesis
"""


from typing import List


CLOSERS = ")}]>"
OPENERS = "({[<"
PAIRS = dict(zip(OPENERS, CLOSERS))


def score(chars: List[str]) -> int:
    key = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    score = 0
    for char in chars:
        score *= 5
        score += key[char]

    return score


def get_missing_chars(line: str) -> List[str]:
    stack = []
    for char in line.strip():
        if char in OPENERS:
            stack.append(char)
        else:
            if not stack:
                return []
            last = stack.pop()
            if PAIRS[last] != char:
                return []
    result = list(map(PAIRS.get, reversed(stack)))
    return result


def solve(input_file: str) -> int:
    results = []
    with open(input_file, "r") as file:
        scores = [score(get_missing_chars(line)) for line in file]

    results = sorted([result for result in scores if result > 0])
    result = results[len(results) // 2]

    print(f"The solution for {input_file!r} is {result}.")

    return result


if __name__ == "__main__":
    test_result = solve("input.test")
    test_answer = 288957
    assert test_result == test_answer
    solve("input.solution")
