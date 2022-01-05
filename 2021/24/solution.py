"""
Advent of Code 2021: Day 24
tldr: ALU stack operations
"""

from typing import List, Tuple


Triple = Tuple[int, int, int]


class ALU:
    def __init__(self, inputs: List[int] = []):
        self.variables = {"w": 0, "x": 0, "y": 0, "z": 0}
        self.inputs = inputs
        self._input_index = 0

    def get_input(self):
        result = self.inputs[self._input_index]
        self._input_index += 1
        return result

    def parse_args(self, a, b):
        val_a = self.variables[a]
        val_b = self.variables[b] if b in self.variables else int(b)
        return val_a, val_b

    def inp(self, variable: int):
        input_value = self.get_input()
        self.variables[variable] = input_value

    def add(self, a, b):
        val_a, val_b = self.parse_args(a, b)
        result = val_a + val_b
        self.variables[a] = result

    def mul(self, a, b):
        val_a, val_b = self.parse_args(a, b)
        result = val_a * val_b
        self.variables[a] = result

    def div(self, a, b):
        val_a, val_b = self.parse_args(a, b)
        result = val_a // val_b
        self.variables[a] = result

    def mod(self, a, b):
        val_a, val_b = self.parse_args(a, b)
        result = val_a % val_b
        self.variables[a] = result

    def eql(self, a, b):
        val_a, val_b = self.parse_args(a, b)
        result = int(val_a == val_b)
        self.variables[a] = result

    def process_line(self, line: str):
        op, *args = line.strip().split(" ")
        func = self.__getattribute__(op)
        func(*args)
        # print(self.variables)

    def process_file(self, input_file: str) -> None:
        with open(input_file, "r") as file:
            for line in file:
                self.process_line(line)
        print(self.variables)
        valid_codes = self.variables["z"] == 0
        return valid_codes


def _get_triples(input_file: str) -> List[Triple]:
    with open(input_file, "r") as file:
        data = [line.strip().split() for line in file.readlines()]

    ops = [4, 5, 15]
    return [tuple(map(lambda x: int(data[i * 18 + x][2]), ops)) for i in range(14)]


def correct_input(inputs: List[int], triples: List[Tuple[int, int, int]]):
    inputs = list(inputs)

    stack = []

    for i in range(14):
        div, chk, add = triples[i]

        if div == 1:
            stack.append((i, add))
        elif div == 26:
            j, add = stack.pop()
            inputs[i] = inputs[j] + add + chk
            if inputs[i] > 9:
                inputs[j] = inputs[j] - (inputs[i] - 9)
                inputs[i] = 9
            if inputs[i] < 1:
                inputs[j] = inputs[j] + (1 - inputs[i])
                inputs[i] = 1
        else:
            raise ValueError(f"{div=}, valid values are 1 and 26")

    return inputs


def solve(input_file: str, inputs: List[int]):
    triples = _get_triples(input_file)
    inputs = correct_input(inputs=inputs, triples=triples)
    alu = ALU(inputs=inputs)
    valid = alu.process_file(input_file=input_file)
    if not valid:
        raise RuntimeError("This input list is not valid")
    result = "".join(map(str, inputs))
    print(f"The solution for {input_file!r} is {result}.")
    return result


def part_one():
    print("part_one")
    solve(input_file="input.solution", inputs=[9] * 14)

def part_two():
    print("part_two")
    solve(input_file="input.solution", inputs=[1] * 14)

def main():
    part_one()
    part_two()

if __name__ == "__main__":
    main()


