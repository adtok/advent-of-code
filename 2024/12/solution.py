from __future__ import annotations

from typing import Generator

EXAMPLE_0 = "example0.txt"
EXAMPLE_1 = "example1.txt"
EXAMPLE_2 = "example2.txt"
INPUT = "input.txt"
FILENAME = EXAMPLE_1


def main() -> None:
    part_one()
    part_two()


def part_one() -> None:
    for filename in [EXAMPLE_0, EXAMPLE_1, EXAMPLE_2]:
        grid = Grid.from_file(filename)
        result = grid.cost()
        print(result)
    grid = Grid.from_file(INPUT)
    result = grid.cost()
    print(result)


def part_two() -> None:
    for filename in [EXAMPLE_0, EXAMPLE_1, EXAMPLE_2]:
        grid = Grid.from_file(filename)
        # grid.show()
        # for region_id in grid._regions:
        #     grid.show(
        #         target={
        #             p: grid.corners(p) if p in grid._regions[region_id] else "#"
        #             for p in grid._grid
        #         }
        #     )
        #     print("*" * grid._width)
        result = grid.cost(bulk_discount=True)
        print(result)
    grid = Grid.from_file(INPUT)
    result = grid.cost(bulk_discount=True)
    print(result)


_directions = [-1j, 1, 1j, -1]


class Plant:
    def __init__(self, label: str) -> None:
        self._label = label
        self.region = None
        self.seen = False

    @property
    def label(self) -> str:
        return self._label


class Grid:
    def __init__(self, grid: dict[complex, str]) -> None:
        self._grid = grid
        height = int(max(grid, key=lambda c: c.imag).imag + 1)
        width = int(max(grid, key=lambda c: c.real).real + 1)
        self._height = height
        self._width = width
        self._plants = {point: Plant(label) for point, label in self._grid.items()}
        region_grid, regions, n_regions = self.calculate_regions(grid, height, width)
        self._region_grid = region_grid
        self._regions = regions
        self._n_regions = n_regions

    def neighboring_points(self, point: complex) -> Generator[complex, None, None]:
        nps = (point + d for d in _directions if point + d in self._grid)
        return nps

    def neighbors(self, point: complex) -> Generator[Plant, None, None]:
        return (self._plants[np] for np in self.neighboring_points(point))

    def calculate_fences(self, point: complex) -> int:
        region_id = self._region_grid[point]
        region = self._regions[region_id]
        neighbors = (point + d for d in _directions)
        result = sum(n not in region or n not in self._grid for n in neighbors)
        return result

    def price(self, region_id: int, bulk_discount: bool = False) -> int:
        if not (region := self._regions.get(region_id)):
            return 0
        perimeter = sum(self.calculate_fences(p) for p in region)
        sides = sum(self.corners(p) for p in region)
        area = len(region)
        result = (sides if bulk_discount else perimeter) * area
        # print(sides if bulk_discount else perimeter, area, result)
        return result

    def cost(self, bulk_discount: bool = False) -> int:
        result = sum(
            self.price(region, bulk_discount=bulk_discount) for region in self._regions
        )
        return result

    def show(self, target: str = None):
        source = self._grid if target is None else target
        for row in range(self._height):
            for col in range(self._width):
                print(source[complex(row, col)], end="")
            print()

    def corners(self, point: complex) -> int:
        curr = self._grid[point]
        region_id = self._region_grid[point]
        region = self._regions[region_id]
        result = 0
        # outer corners
        result += point - 1 not in region and point - 1j not in region
        result += point + 1 not in region and point - 1j not in region
        result += point - 1 not in region and point + 1j not in region
        result += point + 1 not in region and point + 1j not in region
        # inner corners
        result += (
            point - 1 in region
            and point - 1j in region
            and point - 1 - 1j not in region
        )
        result += (
            point + 1 in region
            and point - 1j in region
            and point + 1 - 1j not in region
        )
        result += (
            point - 1 in region
            and point + 1j in region
            and point - 1 + 1j not in region
        )
        result += (
            point + 1 in region
            and point + 1j in region
            and point + 1 + 1j not in region
        )
        return result

    @staticmethod
    def calculate_regions(
        grid: dict[complex, str], height: int, width: int
    ) -> tuple[dict[complex, int], dict[int, set[complex]], int]:
        n_regions = 0
        region_grid: dict[complex, int] = {}
        regions: dict[int, set[complex]] = {}
        for col in range(width):
            for row in range(height):
                point = complex(col, row)
                if point in region_grid:
                    continue
                n_regions += 1
                stack = [point]
                while stack:
                    curr = stack.pop()
                    region_grid[curr] = n_regions
                    if n_regions not in regions:
                        regions[n_regions] = set()
                    regions[n_regions].add(curr)
                    neighbors = (curr + d for d in _directions if curr + d in grid)
                    stack.extend(
                        n
                        for n in neighbors
                        if grid.get(n) == grid[curr] and n not in region_grid
                    )
        return (region_grid, regions, n_regions)

    @classmethod
    def from_file(cls, filename: str) -> Grid:
        with open(filename, "r") as file:
            grid = {
                complex(row, col): value
                for row, line in enumerate(file)
                for col, value in enumerate(line.strip())
            }
        return cls(grid=grid)


if __name__ == "__main__":
    main()
