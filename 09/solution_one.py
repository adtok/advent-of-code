"""
Advent of Code 2021: Day 09 Part 1
tldr: find local minima
"""


from typing import List, Tuple


def read_input(input_file: str) -> List[List[int]]:
    with open(input_file, "r") as file:
        result = [list(map(int, line.strip())) for line in file]
    return result


def find_minima(heatmap: List[List[int]]) -> List[int]:
    height = len(heatmap)
    assert height > 0
    width = len(heatmap[0])

    def get_neighbors(row: int, col: int) -> List[Tuple[int, int]]:
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

    minima: List[int] = []
    for y in range(height):
        for x in range(width):
            reading = heatmap[y][x]
            neighbors = get_neighbors(y, x)

            if all(heatmap[row][col] > reading for row, col in neighbors):
                minima.append(reading)

    return minima


def solve(input_file: str) -> int:
    heatmap = read_input(input_file)
    minima = find_minima(heatmap)

    add_one = lambda val: val + 1
    result = sum(map(add_one, minima))

    print(f"The result for {input_file!r} is {result}.")

    return result


def main():
    test_result = solve("input.test")
    test_answer = 15
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
