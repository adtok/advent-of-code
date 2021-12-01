"""
Advent of Code 2021 Problem 01
tldr: A general solution for any window size
"""
import itertools

from typing import Iterable


# used for debugging
# lines = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def get_increases(lines: Iterable, window_size: int = 1) -> int:
    num_increases = 0
    prev = list(map(int, itertools.islice(lines, window_size)))
    prev_sum = sum(prev)
    for depth_measurement in lines:
        curr = [*prev[1:], int(depth_measurement)]
        curr_sum = sum(curr)
        if curr_sum > prev_sum:
            num_increases += 1
        prev = curr
        prev_sum = curr_sum
    return num_increases


input_file = "input.txt"
for ws in [1, 3]:
    with open(input_file, "r") as lines:
        print(f"Solution with window size {ws}: {get_increases(lines, window_size=ws)}")
