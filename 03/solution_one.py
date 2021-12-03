"""
Advent of Code: Day 03 Part 1
tldr: most prevalent bit
"""


from collections import defaultdict


def bitchar(boolean: bool) -> str:
    return "1" if boolean else "0"


def ZERO() -> int:
    return 0


def solve(input_file):
    tracker = defaultdict(ZERO)
    with open(input_file, "r") as file:
        for count, line in enumerate(file):
            for i, bit_value in enumerate(map(int, line.strip())):
                tracker[i] += int(bit_value)

    thresh = (count + 1) // 2

    gam = int("".join((bitchar(tracker[i] > thresh) for i in range(len(tracker)))), 2)
    eps = int("".join((bitchar(tracker[i] < thresh) for i in range(len(tracker)))), 2)
    result = gam * eps
    print(f"The answer for {input_file!r} is {result}!")
    return result


def main():
    test_result = solve("input.test")
    test_answer = 198
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
