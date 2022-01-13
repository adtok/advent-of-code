"""Advent of Code 2015: Day 6"""


from dataclasses import dataclass
from collections import defaultdict
from enum import Enum, auto
from typing import Tuple



class ModePartOne(Enum):
    ON = lambda v: 1
    OFF = lambda v: 0
    TOGGLE = lambda v: int(not v)

class Mode(Enum):
    ON = lambda v: v + 1
    OFF = lambda v: max(0, v - 1)
    TOGGLE = lambda v: v + 2


def get_mode(string: str) -> Mode:
    mapping = {"on": Mode.ON, "off": Mode.OFF, "toggle": Mode.TOGGLE}
    return mapping[string]


def get_range(string: str) -> range:
    start, stop = map(int, string.split(","))
    return range(start, stop + 1)
    


@dataclass
class Instruction:
    mode: Mode
    range_x: range
    range_y: range

    def points(self):
        yield from ((x, y) for x in self.range_x for y in self.range_y)

    @classmethod
    def from_line(cls, line):
        line = line.split()
        mode = get_mode(line[-4])
        x_0, y_0 = map(int, line[-3].split(","))
        x_1, y_1 = map(int, line[-1].split(","))
        x_r = range(x_0, x_1 + 1)
        y_r = range(y_0, y_1 + 1)
        return cls(mode=mode, range_x=x_r, range_y=y_r)


def read_input(input_file: str):
    with open(input_file, "r") as file:
        for line in file:
            yield line.strip()


def solve(input_file: str):
    lights = defaultdict(int)
    for instruction in map(Instruction.from_line, read_input(input_file)):
        for point in instruction.points():
            value = lights[point]
            lights[point] = instruction.mode(value)

    result = sum(lights.values())

    print(f"The solution is {result}.")

    return result


def main():
    solve("data/06.solution")

if __name__ == "__main__":
    main()