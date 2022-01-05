"""
Advent of Code 2021: Day 21 Part 2
tldr: a dice game with a quantum die
"""


from __future__ import annotations
from collections import defaultdict
from typing import List


def parse_input(input_file: str):
    with open(input_file, "r") as file:
        result = [int(line.split()[-1]) for line in file]
    return result


DIE_ROLLS = [sum((x, y, z)) for z in (1, 2, 3) for y in (1, 2, 3) for x in (1, 2, 3)]


def rolls():
    for roll in DIE_ROLLS:
        yield roll


def move(pos: int, roll: int) -> int:
    return (pos + roll - 1) % 10 + 1


def game(start1, start2):
    p1_wins = 0
    p2_wins = 0
    states = defaultdict(int)
    states[(start1, start2, 0, 0)] = 1
    while states:
        new_states = defaultdict(int)

        for (pos1, pos2, score1, score2), count in states.items():
            for roll in rolls():
                new_pos = move(pos1, roll)
                new_score = score1 + new_pos
                if new_score > 20:
                    p1_wins += count
                else:
                    new_states[(new_pos, pos2, new_score, score2)] += count

        states = new_states
        new_states = defaultdict(int)
        for (pos1, pos2, score1, score2), count in states.items():
            for roll in rolls():
                new_pos = move(pos2, roll)
                new_score = score2 + new_pos
                if new_score > 20:
                    p2_wins += count
                else:
                    new_states[(pos1, new_pos, score1, new_score)] += count
        states = new_states

    return p1_wins, p2_wins


def solve(input_file: str) -> int:
    pos1, pos2 = parse_input(input_file)

    p1_wins, p2_wins = game(pos1, pos2)
    result = max(p1_wins, p2_wins)
    print(f"The solution for {input_file!r} is {result}.")

    return result


def main():
    test_result = solve("input.test")
    test_answer = 444356092776315
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
