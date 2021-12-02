"""
Advent of Code 2021: Day 02 Part 2
tldr: find ending position with a twist
"""

input_file = "input.solution"


hor = 0
ver = 0
aim = 0

with open(input_file, "r") as file:
    for line in file:
        direction, magnitude = line.split()
        magnitude = int(magnitude)
        if direction == "down":
            aim += magnitude
        elif direction == "up":
            aim -= magnitude
        else:
            hor += magnitude
            ver += magnitude * aim

result = ver * hor
print(result)
