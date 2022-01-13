"""Advent of Code 2015: Day 15"""


from dataclasses import dataclass, asdict
from functools import reduce
from typing import Callable, Dict, List


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    @property
    def properties(self) -> Dict[str, int]:
        values = asdict(self)
        del values["name"]
        del values["calories"]
        return values


@dataclass
class Recipe:
    ingredients: List[Ingredient]
    total_space: int

    @property
    def num_ingredients(self):
        return len(self.ingredients)

    @property
    def properties(self):
        Is = [i.properties for i in self.ingredients]
        ps = ["capacity", "durability", "flavor", "texture"]
        result = {p: [i[p] for i in Is] for p in ps}
        return result

    def score(self, quantities: List[int]):
        totals = [
            max(0, sum(v * q for v, q in zip(values, quantities)))
            for values in self.properties.values()
        ]
        return reduce(lambda a, b: a * b, totals)

    def calories(self, quantities: List[int]):
        return sum(i.calories * q for i, q in zip(self.ingredients, quantities))

    def optimize(self, calorie_restriction: int = 0):
        ts = self.total_space
        highest = float("-inf")
        quantities = None
        for i in range(self.total_space):
            for j in range(self.total_space - i):
                for k in range(self.total_space - i - j):
                    h = self.total_space - i - j - k
                    qs = [i, j, k, h]
                    if calorie_restriction and self.calories(qs) != calorie_restriction:
                        continue
                    score = self.score(qs)
                    if score > highest:
                        highest = score
                        quantities = qs

        result = highest
        print(highest, quantities)
        return result


def parse_ingredient(line: str) -> Ingredient:
    name, properties = line.split(": ")
    properties = properties.replace(",", "").split()
    values = dict(zip(properties[::2], map(int, properties[1::2])))
    return Ingredient(name, **values)


def load_ingredients(input_file: str) -> List[Ingredient]:
    with open(input_file, "r") as file:
        ingredients = list(map(parse_ingredient, file))
    return ingredients


def part_one(input_file: str) -> int:
    ingredients = load_ingredients(input_file)
    recipe = Recipe(ingredients, 100)
    result = recipe.optimize()
    return result


def part_two(input_file: str) -> int:
    ingredients = load_ingredients(input_file)
    recipe = Recipe(ingredients, 100)
    result = recipe.optimize(calorie_restriction=500)
    return result


def solve(func: Callable[[str], int]):
    input_file = "data/15.solution"
    result = func(input_file)
    print(f"The solution for {func.__name__!r} is {result}")


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
