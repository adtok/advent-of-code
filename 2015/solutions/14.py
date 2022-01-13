"""Advent of Code 2015: Day 14"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, List


@dataclass(frozen=True)
class Reindeer:
    name: str
    speed: int
    travel_time: int
    rest_time: int

    @property
    def cycle_time(self) -> int:
        return self.travel_time + self.rest_time

    def distance(self, seconds: int) -> float:
        full_cycles = seconds // self.cycle_time
        full_cycle_distance = self.speed * full_cycles * self.travel_time
        extra_time = seconds % self.cycle_time
        extra_distance = self.speed * min(self.travel_time, extra_time)
        return full_cycle_distance + extra_distance

    def is_traveling(self, total_seconds: int):
        seconds = total_seconds % self.cycle_time

    @classmethod
    def parse_line(cls, line: str) -> Reindeer:
        values = line.split()
        return cls(
            name=values[0],
            speed=int(values[3]),
            travel_time=int(values[6]),
            rest_time=int(values[13]),
        )


@dataclass
class Scorer:
    reindeer: List[reindeer]
    scores: Dict[str, int]


def load_reindeer(input_file: str) -> List[Reindeer]:
    with open(input_file, "r") as file:
        result = list(map(Reindeer.parse_line, file))
    return result


def part_one(input_file: str) -> int:
    seconds = 2503
    reindeer = load_reindeer(input_file)
    result = max(map(lambda rd: rd.distance(seconds), reindeer))
    return result


def part_two(input_file: str) -> int:
    seconds = 2503
    reindeer = load_reindeer(input_file)
    scores: Dict[str, int] = {rd.name: 0 for rd in reindeer}

    for second in range(1, seconds + 1):
        leading_distance = max(rd.distance(second) for rd in reindeer)
        for rd in reindeer:
            scores[rd.name] += int(rd.distance(second) == leading_distance)

    winning_reindeer = max(scores, key=scores.get)
    result = scores[winning_reindeer]
    return result


def solve(func: Callable[[str], int]):
    input_file = "data/14.solution"
    result = func(input_file)
    print(f"The solution for {func.__name__!r} is {result}")


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
