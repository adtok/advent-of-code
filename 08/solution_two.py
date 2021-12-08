"""
Advent of Code 2021: Day 07 Part 2
tldr: decode the input and calculate the total
"""


from typing import Dict, List, Tuple


def sort_str(string: str) -> str:
    return "".join(sorted(string))


def parse_line(line: str) -> Tuple[List[str], List[str]]:
    patterns, output = line.strip().split(" | ")
    patterns = list(map(sort_str, patterns.split(" ")))
    output = list(map(sort_str, output.split(" ")))
    return patterns, output


def is_unique(digit: str) -> bool:
    """Returns if a digit can be deduced solely by the length of its representation"""
    return len(digit) in {2, 3, 4, 7}


def not_unique(digit: str) -> bool:
    return not is_unique(digit)


UNIQUE_MAP = {2: 1, 3: 7, 4: 4, 7: 8}
REPEAT_MAP = {10: 2, 11: 5, 12: 6, 13: 3, 14: 0, 15: 9}


def intersection_length(code1: str, code2: str):
    set1 = set(code1)
    set2 = set(code2)
    result = len(set1.intersection(set2))
    return result


def get_uniques(codes: List[str]) -> Dict[str, int]:
    """Generates a key mapping a code to its digit for codes with distinct lengths"""
    codes = [c for c in codes if is_unique(c)]
    result = {code: UNIQUE_MAP[len(code)] for code in codes}
    return result


def get_repeats(codes: List[str], uniques: Dict[str, int]) -> Dict[str, int]:
    """Generates a mapping of a code to its digit for the rest of the codes given a key"""

    def overlapping_sum(code: str) -> int:
        # returns a sum of the intersection length for a code and all unique codes
        return sum(intersection_length(code, unique) for unique in uniques)

    codes = [c for c in codes if not is_unique(c)]
    result = {code: REPEAT_MAP[overlapping_sum(code)] for code in codes}
    return result


def generate_master_key(*codes: List[str]) -> Dict[str, int]:
    uniques = get_uniques(codes)
    assert len(uniques) == 4, "This approach will not work for this input."
    repeats = get_repeats(codes, uniques)
    result = {**uniques, **repeats}
    return result


def solve_line(line: str) -> int:
    patterns, output = parse_line(line)
    master_key = generate_master_key(*patterns, *output)
    string = "".join(map(str, map(master_key.get, output)))
    result = int(string)
    return result


def solve(input_file: str) -> int:
    with open(input_file, "r") as file:
        result = sum(map(solve_line, file))

    print(f"The solution for {input_file!r} is {result}.")

    return result


def main():
    test_result = solve("input.test")
    test_answer = 61229
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
