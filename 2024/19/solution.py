from __future__ import annotations

EXAMPLE = "example0.txt"
INPUT = "input.txt"
FILENAME = INPUT


def main() -> None:
    part_one()
    part_two()


def part_one() -> None:
    rack = Rack.from_file(FILENAME)
    result = sum(rack.possible(design) for design in rack.designs)
    print(f"Part one: {result}")


def part_two() -> None:
    rack = Rack.from_file(FILENAME)
    result = sum(rack.combinations(design) for design in rack.designs)
    print(f"Part two: {result}")


class Rack:
    def __init__(self, patterns: list[str], designs: list[str]) -> None:
        self._patterns = patterns
        self._designs = designs

        # initialize caches with base cases
        self._possible: dict[str, bool] = {"": True}
        self._combinations: dict[str, int] = {"": 1}

    @property
    def patterns(self) -> list[str]:
        return self._patterns

    @property
    def designs(self) -> list[str]:
        return self._designs

    def possible(self, design: str) -> bool:
        if design in self._possible:
            return self._possible[design]
        result = any(
            self.possible(design[len(pattern) :])
            for pattern in self.patterns
            if design.startswith(pattern)
        )
        self._possible[design] = result
        return result

    def slow_combos(self, design: str) -> int:
        if design in self._combinations:
            return self._combinations[design]
        result = sum(
            self.slow_combos(design[len(pattern) :])
            for pattern in self.patterns
            if design.startswith(pattern)
        )
        self._possible[design] = result
        return result

    def combinations(self, design: str) -> int:
        if design in self._combinations:
            return self._combinations[design]
        result = sum(
            self.combinations(design.removeprefix(pattern))
            for pattern in self.patterns
            if design.startswith(pattern)
        )
        self._combinations[design] = result
        return result

    @classmethod
    def from_file(cls, filename: str) -> Rack:
        patterns, designs = parse(filename)
        result = cls(patterns, designs)
        return result


def parse(filename: str) -> tuple[list[str], list[str]]:
    with open(filename, "r") as file:
        patterns = next(file).strip().split(", ")
        next(file)
        designs = list(map(str.strip, file))
    result = patterns, designs
    return result


if __name__ == "__main__":
    main()
