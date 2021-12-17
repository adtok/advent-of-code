"""
Advent of Code 2021: Day 17 Part 1
tldr: kinematics
"""


from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class Vec:
    x: int
    y: int


@dataclass
class Target:
    start: Vec
    end: Vec


@dataclass
class Probe:
    pos: Vec
    vel: Vec
    target: Target
    highest_point: int = 0

    @property
    def in_x(self) -> bool:
        return self.target.start.x <= self.pos.x <= self.target.end.x

    @property
    def in_y(self) -> bool:
        return self.target.start.y <= self.pos.y <= self.target.end.y

    @property
    def in_target(self) -> bool:
        return self.in_x and self.in_y

    @property
    def missed(self) -> bool:
        return self.pos.y < self.target.start.y

    def step(self) -> None:
        pos_x = self.pos.x + self.vel.x
        pos_y = self.pos.y + self.vel.y
        vel_x = max(0, self.vel.x - 1)
        vel_y = self.vel.y - 1
        self.pos = Vec(pos_x, pos_y)
        self.vel = Vec(vel_x, vel_y)
        self.highest_point = max(self.highest_point, self.pos.y)


target = Target(start=Vec(20, -10), end=Vec(30, -5))
probe = Probe(pos=Vec(0, 0), vel=Vec(7, 2), target=target)


def parse_input(input_file: str) -> Tuple[int, int, int, int]:
    with open(input_file, "r") as file:
        line = file.read().strip()
    data = line[13:]
    x_data, y_data = data.split(", ")
    x1, x2 = list(map(int, x_data[2:].split("..")))
    y1, y2 = list(map(int, y_data[2:].split("..")))
    return x1, x2, y1, y2


def solve(input_file: str) -> int:
    tx0, tx1, ty0, ty1 = parse_input(input_file)

    target = Target(start=Vec(tx0, ty0), end=Vec(tx1, ty1))

    highest_point_map: Dict[Vec, int] = {}
    for vy0 in range(-100, 100):
        for vx0 in range(0, 100):
            initial_pos = Vec(0, 0)
            initial_vel = Vec(vx0, vy0)
            probe = Probe(initial_pos, initial_vel, target)
            while not probe.missed:
                probe.step()
                if probe.in_target:
                    highest_point_map[initial_vel] = probe.highest_point
                    break

    highest_point = max(highest_point_map.values())

    result = highest_point
    print(f"The solution to {input_file!r} is {result}.")
    return result


def main():
    test_result = solve("input.test")
    test_answer = 45
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
