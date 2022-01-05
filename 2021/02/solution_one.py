"""
Advent of Code 2021: Day 02 Part 1
tldr: Find two dimensional ending position
"""


input_file = "input.solution"


totals = {
    "forward": 0,
    "down": 0,
    "up": 0,
}


with open(input_file, "r") as file:
    for line in file:
        direction, magnitude = line.split()
        totals[direction] += int(magnitude)

result = (totals["down"] - totals["up"]) * totals["forward"]
print(result)
