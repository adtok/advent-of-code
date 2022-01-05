"""
Advent of Code 2021: Day 16 Part 2
tldr: parsing packets and doing operations
"""

from dataclasses import dataclass
from functools import reduce
from typing import List, Protocol, Tuple


@dataclass
class Packet(Protocol):

    version: int
    type_id: int

    def version_sum(self) -> int:
        ...

    @property
    def value(self) -> int:
        ...


@dataclass
class LiteralValuePacket(Packet):

    _value: int

    def version_sum(self) -> int:
        return self.version

    @property
    def value(self) -> int:
        return self._value


@dataclass
class OperatorPacket(Packet):

    length_type: int
    length: int
    packets: List[Packet]

    def version_sum(self) -> int:
        return sum(packet.version_sum() for packet in self.packets) + self.version

    @property
    def values(self) -> int:
        return [p.value for p in self.packets]

    @property
    def value(self) -> int:
        if self.type_id == 0:
            return sum(self.values)
        if self.type_id == 1:
            return reduce(lambda a, b: a * b, self.values, 1)
        if self.type_id == 2:
            return min(self.values)
        if self.type_id == 3:
            return max(self.values)
        if self.type_id == 4:
            raise ValueError
        if self.type_id == 5:
            assert len(self.packets) == 2
            p1, p2 = self.packets
            return int(p1.value > p2.value)
        if self.type_id == 6:
            assert len(self.packets) == 2
            p1, p2 = self.packets
            return int(p1.value < p2.value)
        if self.type_id == 7:
            assert len(self.packets) == 2
            p1, p2 = self.packets
            return int(p1.value == p2.value)
        raise ValueError(f"Packet type {self.type_id} not supported.")


def hex_to_binary(value: str) -> str:
    return bin(int(value, 16))[2:].zfill(len(value) * 4)


def read_packet(bits: str) -> Tuple[Packet, str]:
    version = int(bits[:3], 2)
    type_id = int(bits[3:6], 2)

    if type_id == 4:
        num = ""
        for i in range(6, len(bits), 5):
            num += bits[i + 1 : i + 5]
            if bits[i] == "0":
                break
        value = int(num, 2)
        packet = LiteralValuePacket(version=version, type_id=type_id, _value=value)
        return packet, bits[i + 5 :]

    length_type = int(bits[6])
    subpackets = []

    if length_type == 0:
        length = int(bits[7:22], 2)
        subpacket_bits = bits[22 : 22 + length]
        while subpacket_bits:
            subpacket, subpacket_bits = read_packet(subpacket_bits)
            subpackets.append(subpacket)
        bits = bits[22 + length :]
    else:
        length = int(bits[7:18], 2)
        bits = bits[18:]
        for _ in range(length):
            subpacket, new_bits = read_packet(bits)
            subpackets.append(subpacket)
            bits = new_bits

    return (
        OperatorPacket(
            version=version,
            type_id=type_id,
            length_type=length_type,
            length=length,
            packets=subpackets,
        ),
        bits,
    )


def solve(input_value: str) -> int:
    binary = hex_to_binary(input_value)
    packet, _ = read_packet(binary)
    result = packet.value

    print(f"The solution for {input_value[:20]!r}... is {result}.")
    return result


def main():
    with open("input.test_part2") as file:
        test_results = (3, 54, 7, 9, 1, 0, 0, 1)
        for line, test_answer in zip(file, test_results):
            test_result = solve(line.strip())
            assert test_result == test_answer

    print("\nSolution for personal input below:")

    with open("input.solution") as file:
        solution_input = file.read().strip()

    solve(solution_input)


if __name__ == "__main__":
    main()
