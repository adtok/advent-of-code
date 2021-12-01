"""
Advent of Code 2021 Problem 01
tldr: A general solution for any window size
"""

input_file = "input.txt"

with open(input_file, "r") as fi:
    lines = list(map(int, fi.readlines()))

# used for debugging
# lines = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

def get_increases(lines, window_size=1):
    num_increases = 0
    n = len(lines)
    prev = sum(lines[0:window_size])
    for i in range(window_size + 1, n + 1):
        curr = sum(lines[i - window_size : i])
        if curr > prev:
            num_increases += 1
        prev = curr
    return num_increases


for ws in [1, 3]:
    print(f"Solution with window size {ws}: {get_increases(lines, window_size=ws)}")
