"""Advent of Code 2015: Day 23"""


from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Protocol


class Instruction(Protocol):
    name: str = ""

    @staticmethod
    def execute(computer: Computer, register: str, offset: int = 0) -> int:
        ...


class Half(Instruction):
    name: str = "hlf"

    @staticmethod
    def execute(computer: Computer, register: str, offset: int = 0) -> int:
        value = computer.get_register(register) // 2
        computer.set_register(register, value)
        computer.increment_pointer()
        return value


class Triple(Instruction):
    name: str = "tpl"

    @staticmethod
    def execute(computer: Computer, register: str, offset: int = 0) -> int:
        value = computer.get_register(register) * 3
        computer.set_register(register, value)
        computer.increment_pointer()
        return value


class Increment(Instruction):
    name: str = "inc"

    @staticmethod
    def execute(computer: Computer, register: str, offset: int = 0) -> int:
        value = computer.get_register(register) + 1
        computer.set_register(register, value)
        computer.increment_pointer()
        return value


class Jump(Instruction):
    name: str = "jmp"

    @staticmethod
    def execute(computer: Computer, register: str, offset: int = 0) -> int:
        computer.jump(offset)
        return computer.get_pointer()


class JumpIfEven(Instruction):
    name: str = "jie"

    @staticmethod
    def execute(computer: Computer, register: str, offset: int = 0) -> int:
        if computer.get_register(register) % 2 == 0:
            computer.jump(offset)
        else:
            computer.increment_pointer()
        return computer.get_pointer()


class JumpIfOne(Instruction):
    name: str = "jio"

    @staticmethod
    def execute(computer: Computer, register: str, offset: int = 0) -> int:
        if computer.get_register(register) == 1:
            computer.jump(offset)
        else:
            computer.increment_pointer()
        return computer.get_pointer()


@dataclass
class Computer:
    program: List[str]
    program_size: int = field(init=False)
    registers: Dict[str, int] = field(
        default_factory=lambda: {"a": 0, "b": 0}, init=False
    )
    pointer: int = field(default=0, init=False)

    def __post_init__(self):
        self.program_size = len(self.program)

    def get_pointer(self):
        return self.pointer

    def increment_pointer(self):
        self.pointer += 1

    def jump(self, offset: int):
        self.pointer += offset

    def current_instruction(self):
        return self.program[self.pointer]

    def get_register(self, register: str) -> int:
        return self.registers[register]

    def set_register(self, register: str, value: int) -> int:
        self.registers[register] = value
        return value

    def run_instruction(self):
        program_instruction = self.current_instruction()
        name = program_instruction[:3]
        params = program_instruction[4:]
        register = None
        offset = 0
        if name in {"jie", "jio"}:
            register, offset = params.split(", ")
            offset = int(offset)
        elif name == "jmp":
            offset = int(params)
        else:
            register = params

        instruction = next((i for i in Instruction.__subclasses__() if i.name == name))
        instruction.execute(computer=self, register=register, offset=offset)

    def run_program(self):
        while self.pointer < self.program_size:
            self.run_instruction()
        print(self.registers)

    @classmethod
    def from_file(cls, input_file: str) -> Computer:
        with open(input_file, "r") as file:
            program = list(map(str.strip, file))
        return cls(program=program)


def part_one(input_file: str) -> int:
    computer = Computer.from_file(input_file)
    computer.run_program()
    result = computer.get_register("b")
    return result


def part_two(input_file: str) -> int:
    computer = Computer.from_file(input_file)
    computer.set_register("a", 1)
    computer.run_program()
    result = computer.get_register("b")
    return result


def solve(func: Callable[[str], int]):
    input_file = "data/23.solution"
    result = func(input_file)
    print(f"The solution for {func.__name__!r} is {result}")


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
