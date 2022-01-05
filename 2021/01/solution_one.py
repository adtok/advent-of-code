"""
Advent of Code 2021 Problem 01 Part 1
tldr: count the number of times a depth measurement increases
"""

input_file = "input.txt"

num_increases = 0

with open(input_file, "r") as fi:
    prev = int(next(fi))
    for line in fi:
        curr = int(line)
        if curr > prev:
            num_increases += 1
        prev = curr

print(num_increases)
