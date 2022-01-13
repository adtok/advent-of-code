"""Advent of Code 2015: Day 1"""

from collections import Counter

with open("data/01.solution") as file:
    data = file.read().strip()

def floor(string: str) -> int:
    counter = Counter(string)
    return counter["("] - counter[")"]


part_one = floor(data)

part_two = list(map(floor, (data[:i+1] for i in range(len(data))))).index(-1)

print(f"{part_one=}, {part_two=}")