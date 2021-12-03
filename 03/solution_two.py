"""
Advent of Code: Day 03 Part 2
tldr: most prevalent bit at a position, paring down as we go
"""


from typing import List, Tuple


def bitchar(boolean: bool) -> str:
    return "1" if boolean else "0"


def most_common_bit(lines: List[str], position: int) -> str:
    ones = sum(int(line[position]) for line in lines)
    zeros = len(lines) - ones
    return bitchar(ones >= zeros)


def least_common_bit(lines: List[str], position: int) -> str:
    ones = sum(int(line[position]) for line in lines)
    zeros = len(lines) - ones
    return bitchar(ones < zeros)


def solve(input_file: str) -> int:
    with open(input_file, "r") as file:
        lines = [line.strip() for line in file]

    assert len(lines) > 0

    num_bits = len(lines[0])

    ogr_lines = csr_lines = lines
    for position in range(num_bits):
        mcb = most_common_bit(ogr_lines, position)
        if len(ogr_lines) > 1:
            ogr_lines = [line for line in ogr_lines if line[position] == mcb]

        lcb = least_common_bit(csr_lines, position)
        if len(csr_lines) > 1:
            csr_lines = [line for line in csr_lines if line[position] == lcb]

    assert len(ogr_lines) == 1
    assert len(csr_lines) == 1

    ogr = int(csr_lines[0], 2)
    csr = int(ogr_lines[0], 2)

    lsr = ogr * csr
    print(f"The solution for {input_file!r} is {lsr}!")
    return lsr


def main():
    test_result = solve("input.test")
    test_answer = 230
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
