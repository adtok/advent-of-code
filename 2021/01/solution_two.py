"""
Advent of Code 2021 Problem 01 Part 2
tldr: count depth increases based on a sliding window
"""

input_file = "input.txt"

with open(input_file, "r") as fi:
    lines = list(map(int, fi.readlines()))

# used for debugging
# lines = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

num_increases = 0
n = len(lines)
prev = sum(lines[0:3])
for i in range(4, n + 1):
    curr = sum(lines[i - 3 : i])
    if curr > prev:
        num_increases += 1
    prev = curr

print(num_increases)
