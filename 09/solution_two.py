"""
Advent of Code 2021: Day 09 Part 1
tldr: graph traversal to find basins
"""

from functools import reduce
from typing import List, Set, Tuple


Point = Tuple[int, int]
Map = List[List[int]]


def read_input(input_file: str) -> Map:
    """Reads the input file into a list of lists of integers"""
    with open(input_file, "r") as file:
        result = [list(map(int, line.strip())) for line in file]
    return result


def get_neighbors(row: int, col: int, height: int, width: int) -> List[Point]:
    """Get the neighbors for a coordinate"""
    neighbors: List[int] = []

    if row != 0:
        neighbors.append((row - 1, col))
    if col != 0:
        neighbors.append((row, col - 1))
    if row != height - 1:
        neighbors.append((row + 1, col))
    if col != width - 1:
        neighbors.append((row, col + 1))

    return neighbors


def find_minima(heatmap: Map, height: int, width: int) -> List[Point]:
    """Returns a list of coordinates with the local minima for a heatmap"""
    minima: List[int] = []
    for y in range(height):
        for x in range(width):
            reading = heatmap[y][x]
            neighbors = get_neighbors(y, x, height, width)

            if all(heatmap[row][col] > reading for row, col in neighbors):
                minima.append((y, x))

    return minima


def get_basin(
    heatmap: Map, height: int, width: int, initial_point: Point
) -> List[Point]:
    points: List[Point] = [initial_point]
    visited: Set[Point] = set()
    basin: List[Tuple[int]] = [initial_point]
    while points:
        point_p = y_p, x_p = points.pop()
        for point_n in get_neighbors(y_p, x_p, height, width):
            if point_n in visited:
                continue
            y_n, x_n = point_n
            reading_n = heatmap[y_n][x_n]
            if reading_n != 9 and point_n not in basin:
                points = [point_n] + points
                basin.append(point_n)
        visited.add(point_p)

    return basin


def solve(input_file: str) -> int:
    """Solves the puzzle for an input"""
    heatmap = read_input(input_file)
    height = len(heatmap)
    assert height > 0
    width = len(heatmap[0])
    assert width > 0
    minima = find_minima(heatmap, height, width)
    basins = [get_basin(heatmap, height, width, point) for point in minima]

    biggest_basins = sorted(basins, key=len, reverse=True)[:3]
    sizes = [len(basin) for basin in biggest_basins]
    result = reduce(lambda s1, s2: s1 * s2, sizes, 1)

    print(f"The result for {input_file!r} is {result}.")

    return result


def main():
    test_result = solve("input.test")
    test_answer = 1134
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
