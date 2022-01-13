"""
Advent of Code 2015: Day 3
"""

from collections import defaultdict
from typing import Tuple


Point = Tuple[int, int]

def _parse_input(input_file: str) -> str:
    with open(input_file, "r") as file:
        result = file.read().strip()
    return result


def move(point: Point, change: Point) -> Point:
    x, y = point
    dx, dy = change
    result = (x + dx, y + dy)
    return result

MOVE_MAPPING = {"^": (0, 1), ">": (1, 0), "v": (0, -1), "<": (-1, 0)}

def part_1(input_file: str):
    data = _parse_input(input_file)
    locations = defaultdict(int)
    position = (0, 0)
    locations[position] += 1
    for direction in data:
        dxdy = MOVE_MAPPING.get(direction)
        position = move(position, dxdy)
        locations[position] += 1
    
    print(f"Solution for part 1: {len(locations)}")


def part_2(input_file: str):
    data = _parse_input(input_file)
    presents_delivered = defaultdict(int)
    location_s = (0, 0)
    location_r = (0, 0)
    presents_delivered[location_s] += 2
    instructions_s = data[::2]
    instructions_r = data[1::2]

    for dir_s, dir_r in zip(instructions_s, instructions_r):
        dxdy_s = MOVE_MAPPING.get(dir_s)
        dxdy_r = MOVE_MAPPING.get(dir_r)
        location_s = move(location_s, dxdy_s)
        location_r = move(location_r, dxdy_r)
        presents_delivered[location_s] += 1
        presents_delivered[location_r] += 1

    print(f"solution to part 2: {len(presents_delivered)}")

def solve(input_file: str):
    part_1(input_file)
    part_2(input_file)

def main():
    solve("data/03.solution")

if __name__ == "__main__":
    main()