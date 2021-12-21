"""
Advent of Code 2021: Day 20 Part 1
tldr: ENHANCE!
"""


from dataclasses import dataclass
from typing import List


DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]


Image = List[List[str]]


def neighbors(r, c):
    for dr, dc in DIRS:
        yield (r + dr, c + dc)


def in_bounds(y: int, x: int, h: int, w: int) -> bool:
    return 0 <= y < h and 0 <= x < w


def to_int(value: str) -> int:
    binary = "".join(str(int(c == "#")) for c in value)
    return int(binary, 2)


@dataclass
class Enhancer:
    algorithm: str
    original_image: Image
    images: List[Image]

    @classmethod
    def from_file(cls, input_file: str):
        with open(input_file, "r") as file:
            algorithm, lines = file.read().split("\n\n")

        lines = list(map(list, lines.splitlines()))

        return cls(algorithm=algorithm, original_image=lines, images=[lines])

    def enhance(self, times: int) -> None:
        inf_space = "."

        for _ in range(times):
            image = self.images[-1]
            rows = len(image)
            cols = len(image[0])

            enhanced_image = [["." for _ in range(cols + 2)] for _ in range(rows + 2)]

            for row in range(-1, rows + 1):
                for col in range(-1, cols + 1):
                    surroundings = ""
                    for r, c in neighbors(row, col):
                        surroundings += (
                            image[r][c] if in_bounds(r, c, rows, cols) else inf_space
                        )
                    value = to_int(surroundings)
                    enhanced_image[row + 1][col + 1] = self.algorithm[value]

            inf_space = self.algorithm[to_int(inf_space * 9)]

            self.images.append(enhanced_image)

        return sum(line.count("#") for line in self.images[-1])


def solve(input_file: str, times: int) -> int:
    en = Enhancer.from_file(input_file)
    result = en.enhance(times)

    print(f"Enhancing {input_file!r} with {times=} yields {result=}.")
    return result


def main():
    # part 1
    test_result = solve("input.test", 2)
    test_answer = 35
    assert test_result == test_answer
    solve("input.solution", 2)

    # part 2
    test_result = solve("input.test", 50)
    test_answer = 3351
    assert test_result == test_answer
    solve("input.solution", 50)


if __name__ == "__main__":
    main()
