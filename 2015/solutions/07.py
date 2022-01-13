"""Advent of Code 2015: Day 7"""


from dataclasses import dataclass, field
from typing import Dict, List



def NOT(value: int) -> int:
    result = int("".join(map(str, map(lambda v: int(not v), map(int, bin(value)[2:].zfill(16))))), 2)
    return result



@dataclass
class Computer:
    inputs: Dict[str, List[str]]
    variables: Dict[str, int] = field(default_factory=dict)

    def set(self, target: str, value: int):
        self.variables[target] = value

    def get(self, variable: str) -> int:
        if variable not in self.variables:
            self.run_instruction(self.inputs[variable])
        return self.variables[variable]

    def val(self, string: str):
        if string.isnumeric():
            return int(string)
        return self.get(string)

    def run_instruction(self, values: List[str]):

        target = values[-1]
        if len(values) == 3:
            value = self.val(values[0])
            self.set(target, value)
        elif len(values) == 4:
            value = self.val(values[1])
            self.set(target, NOT(value))
        elif len(values) == 5:
            one = self.val(values[0])
            two = self.val(values[2])
            operation = values[1]
            value = None
            if operation == "AND":
                value = one & two
            elif operation == "OR":
                value = one | two
            elif operation == "LSHIFT":
                value = one << two
            elif operation == "RSHIFT":
                value = one >> two
            else:
                raise ValueError(f"{operation} is not implemented")
            if value is None:
                raise ValueError(f"{operation=} {one=} {two=} caused an error")
            self.set(target, value)
            

def main(input_file: str):
    with open(input_file, "r") as file:
        instructions = [line.split() for line in file]

    inputs = {instruction[-1]: instruction for instruction in instructions}
    computer = Computer(inputs=inputs)
    result = computer.get("a")
    print(f"The solution for part one is {result}")
    new_computer = Computer(inputs=inputs)
    new_computer.set("b", result)
    result = new_computer.get("a")
    print(f"The solution for part two is {result}")

if __name__ == "__main__":
    main("data/07.solution")