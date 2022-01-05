"""
Advent of Code 2021: Day 21 Part 1
tldr: a dice game
"""


from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class Player:
    position: int
    score: int = 0

    def move(self, rolls: List[int]):
        distance = sum(rolls)
        new_position = (self.position + distance - 1) % 10 + 1
        self.score += new_position
        self.position = new_position
        return new_position


@dataclass
class Die:
    value: int = 1
    total_rolls: int = 0

    def roll(self, amount: int = 1) -> List[int]:
        if amount < 1:
            raise ValueError
        rolls = []
        for _ in range(amount):
            rolls.append(self.value)
            self.value += 1
            if self.value > 100:
                self.value = 1
            self.total_rolls += 1

        return rolls


@dataclass
class Game:
    players: List[Player]
    die: Die = field(default_factory=Die)

    @classmethod
    def from_positions(cls, pos1: int, pos2: int) -> Game:
        player1 = Player(position=pos1)
        player2 = Player(position=pos2)
        return cls(players=[player1, player2])

    def loop(self, roll_size: int = 3) -> List[int]:
        active_player = 0
        while self.players[0].score < 1000 and self.players[1].score < 1000:
            rolls = self.die.roll(amount=roll_size)
            score = self.players[active_player].move(rolls=rolls)
            print(f"{active_player=} {score=} {self.players[active_player]}")
            active_player = (active_player + 1) % 2

        return [player.score for player in self.players]


def parse_input(input_file: str):
    with open(input_file, "r") as file:
        result = [int(line.split()[-1]) for line in file]
    print(result)
    return result


def solve(input_file: str) -> int:
    pos1, pos2 = parse_input(input_file)
    game = Game.from_positions(pos1=pos1, pos2=pos2)

    _, sc2 = game.loop(roll_size=3)
    result = sc2 * game.die.total_rolls

    print(f"The solution for {input_file!r} is {result}.")

    return result


def main():
    test_result = solve("input.test")
    test_answer = 739785
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
