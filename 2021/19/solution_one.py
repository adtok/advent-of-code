"""
Advent of Code 2021: Day 19 Part 1
tldr: overlapping scanner coordinates
"""

from __future__ import annotations
from dataclasses import dataclass, field
from itertools import combinations
from typing import Dict, List, Optional, Set, Tuple


ROTATIONS = [
    ([2, 0, 1], [-1, -1, 1]),
    ([0, 1, 2], [1, -1, -1]),
    ([2, 1, 0], [-1, -1, -1]),
    ([2, 1, 0], [1, -1, 1]),
    ([0, 2, 1], [-1, -1, -1]),
    ([1, 2, 0], [1, -1, -1]),
    ([1, 0, 2], [-1, -1, -1]),
    ([1, 2, 0], [1, 1, 1]),
    ([0, 2, 1], [-1, 1, 1]),
    ([0, 1, 2], [-1, 1, -1]),
    ([0, 2, 1], [1, -1, 1]),
    ([2, 0, 1], [-1, 1, -1]),
    ([1, 0, 2], [1, 1, -1]),
    ([2, 1, 0], [1, 1, -1]),
    ([2, 0, 1], [1, 1, 1]),
    ([2, 1, 0], [-1, 1, 1]),
    ([0, 1, 2], [1, 1, 1]),
    ([1, 0, 2], [1, -1, 1]),
    ([1, 0, 2], [-1, 1, 1]),
    ([0, 1, 2], [-1, -1, 1]),
    ([1, 2, 0], [-1, 1, -1]),
    ([1, 2, 0], [-1, -1, 1]),
    ([0, 2, 1], [1, 1, -1]),
    ([2, 0, 1], [1, -1, -1]),
]

def rotations():
    for rotation in ROTATIONS:
        yield rotation


@dataclass
class Point:
    x: int
    y: int
    z: int


def rotate(point: Point, rotation: Tuple[List[int], List[int]]) -> Point:
    tmp = (point.x, point.y, point.z)
    (a0, a1, a2), (f0, f1, f2) = rotation
    x = tmp[a0] * f0
    y = tmp[a1] * f1
    z = tmp[a2] * f2
    return Point(x=x, y=y, z=z)


def euclidean_distance(p1: Point, p2: Point):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dz = p1.z - p2.z

    return int((dx * dx + dy * dy + dz * dz) ** 2)





@dataclass
class Scanner:
    label: int
    points: List[Point]
    _distances: List[Tuple[int, int, int]] = field(default_factory=list)
    position: Optional[Point] = None

    def f(self):
        return 1

    def distances(self) -> Set[Tuple[int, int, int]]:
        distances = set()
        for p1, p2 in zip(self.points, self.points[1:]):
            distances.add(euclidean_distance(p1, p2))
        return distances


def parse_point(line: str) -> Point:
    x, y, z = list(map(int, line.split(",")))
    return Point(x=x, y=y, z=z)

    


def parse_scanner(scanner_text: List[str]) -> Tuple[int, List[Point]]:
    header, *points_text = scanner_text.splitlines()
    label = int(header.split(" ")[2])
    points = list(map(parse_point, points_text))
    # return Scanner(label=label, points=points)
    return label, points


def solve(input_file: str) -> int:
    with open(input_file, "r") as file:
        scanners_input = file.read().split("\n\n")
    scanners: Dict[int, List[Point]] = {label: points for label, points in map(parse_scanner, scanners_input)}

    intersections = get_intersections(scanners)
    print(intersections)


    return -1


def get_intersections(scanners: Dict[int, List[Point]]):
    intersections = []
    distance_dict = {i: set(euclidean_distance(p1, p2) for p1, p2 in combinations(scanners[i], 2)) for i in scanners}
    for i, j in combinations(range(len(scanners)), 2):
        if len(distance_dict[i].intersection(distance_dict[j])) >= 66:
            intersections.append((i, j))
            intersections.append((j, i))
    return intersections


def main():
    point = Point(1, 2, 3)
    for rotation in ROTATIONS:
        p = rotate(point, rotation)
        print(rotation, p)
    test_result = solve("input.test")
    test_answer = 79
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
