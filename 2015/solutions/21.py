"""Advent of Code 2015: Day 21"""

from __future__ import annotations
from dataclasses import dataclass, field
from itertools import combinations
from enum import Enum, auto
from typing import Callable, List

# Name / Cost / Damage/ Armor (data/21.shop)
DATA = {
    "weapons": [
        ("Dagger", 8, 4, 0),
        ("Shortsword", 10, 5, 0),
        ("Warhammer", 25, 6, 0),
        ("Longsword", 40, 7, 0),
        ("Greataxe", 74, 8, 0),
    ],
    "armor": [
        ("Leather", 13, 0, 1),
        ("Chainmail", 31, 0, 2),
        ("Splintmail", 53, 0, 3),
        ("Bandedmail", 75, 0, 4),
        ("Platemail", 102, 0, 5),
    ],
    "rings": [
        ("Damage +1", 25, 1, 0),
        ("Damage +2", 50, 2, 0),
        ("Damage +3", 100, 3, 0),
        ("Defense +1", 20, 0, 1),
        ("Defense +2", 40, 0, 2),
        ("Defense +3", 80, 0, 3),
    ],
}


class Slot(Enum):
    WEAPON = auto()
    ARMOR = auto()
    RING = auto()


@dataclass
class Equipment:
    name: str
    cost: int
    damage: int
    armor: int
    slot: Slot


@dataclass
class Character:
    name: str
    max_hitpoints: int
    base_damage: int
    base_armor: int
    equipment: List[Equipment] = field(default_factory=list)
    current_hp: int = field(init=False)

    def __post_init__(self):
        self.current_hp = self.max_hitpoints

    @property
    def damage(self):
        return self.base_damage + sum(e.damage for e in self.equipment)

    @property
    def armor(self):
        return self.base_armor + sum(e.armor for e in self.equipment)

    def attack(self, other: Character, verbose: bool = False):
        dmg_dealt = max(1, self.damage - other.armor)
        other.current_hp = max(0, other.current_hp - dmg_dealt)
        if verbose:
            print(
                f"The {self.name} dealt {dmg_dealt} to {other.name} (now at {other.current_hp})."
            )
        return other.current_hp


WEAPONS = [Equipment(n, c, d, a, Slot.WEAPON) for n, c, d, a in DATA["weapons"]]
ARMOR = [Equipment(n, c, d, a, Slot.ARMOR) for n, c, d, a in DATA["armor"]]
RINGS = [Equipment(n, c, d, a, Slot.RING) for n, c, d, a in DATA["rings"]]

PLAYER_STATS = {
    "name": "Player",
    "max_hitpoints": 100,
    "base_damage": 0,
    "base_armor": 0,
}
BOSS_STATS = {
    "name": "Big Bad Boss",
    "max_hitpoints": 104,
    "base_damage": 8,
    "base_armor": 1,
}


def battle(player: Character, boss: Character):

    winner = None
    while player.current_hp > 0 and boss.current_hp > 0:
        boss_hp = player.attack(boss)
        if boss_hp <= 0:
            return player
        player_hp = boss.attack(player)
        if player_hp <= 0:
            return boss
    print(f"The winner is {winner.name}.")
    return winner


def generate_equipment_set():
    for weapon in WEAPONS:
        for num_armor in [0, 1]:
            for armors in combinations(ARMOR, num_armor):
                for num_rings in [0, 1, 2]:
                    for rings in combinations(RINGS, num_rings):
                        equipment = [weapon] + list(armors) + list(rings)
                        yield equipment


def part_one(_: str) -> int:
    lowest_cost = float("inf")
    for equipment in generate_equipment_set():
        total_cost = sum(e.cost for e in equipment)
        if total_cost < lowest_cost:
            player = Character(**PLAYER_STATS, equipment=equipment)
            boss = Character(**BOSS_STATS)
            winner = battle(player, boss)
            if winner.name == "Player":
                lowest_cost = min(lowest_cost, total_cost)
    return lowest_cost


def part_two(_: str) -> int:
    highest = float("-inf")
    for equipment in generate_equipment_set():
        total_cost = sum(e.cost for e in equipment)
        if total_cost > highest:
            player = Character(**PLAYER_STATS, equipment=equipment)
            boss = Character(**BOSS_STATS)
            winner = battle(player, boss)
            if winner.name == "Big Bad Boss":
                highest = max(highest, total_cost)
    return highest


def solve(func: Callable[[str], int]):
    input_file = "data/21.solution"
    result = func(input_file)
    print(f"The solution for {func.__name__!r} is {result}")


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
