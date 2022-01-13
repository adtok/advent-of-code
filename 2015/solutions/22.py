"""Advent of Code 2015: Day 21"""

from __future__ import annotations
from dataclasses import dataclass, field
from itertools import combinations
from typing import Callable, Dict, Generator, List, Optional, Protocol


PLAYER_STATS = {
    "name": "Player",
    "max_hitpoints": 50,
}
BOSS_STATS = {
    "name": "Big Bad Boss",
    "max_hitpoints": 58,
    "base_damage": 9,
}


@dataclass
class Spell:
    name: str
    mana_cost: int = 0
    duration: int = 0
    damage: int = 0
    heal: int = 0
    shield: int = 0
    recharge: int = 0
    timer: int = 0

    def cast(self, caster: Character, other: Character) -> int:
        if caster.current_mana < self.mana_cost:
            raise ValueError("The caster does not have enough mana.")
        if self.timer > 0:
            raise ValueError(f"The caster has {self.name} active already.")
        print(f"Casting {self.name}.")
        caster.current_mana -= self.mana_cost
        caster.mana_spent += self.mana_cost
        if self.duration > 0:
            return self.start_timer()
        return self.resolve_effect(caster, other)

    def start_timer(self) -> int:
        self.timer = self.duration
        return self.timer

    def resolve_effect(self, caster: Character, other: Character) -> int:
        if self.timer > 0:
            self.timer -= 1
        return self.effect(caster, other)

    def effect(self, caster: Character, other: Character) -> int:
        other.take_damage(self.damage)
        caster.heal(self.heal)
        caster.recharge(self.recharge)


@dataclass
class Effect:
    spell: int
    duration: int = 0
    timer: int = 0


@dataclass
class MagicMissile(Spell):
    name: str = "Magic Missile"
    mana_cost: int = 53
    damage: int = 4


@dataclass
class Drain(Spell):
    name: str = "Drain"
    mana_cost: int = 73
    damage: int = 2
    heal: int = 2


@dataclass
class Shield(Spell):
    name: str = "Shield"
    mana_cost: int = 113
    duration: int = 6
    shield: int = 7


@dataclass
class Poison(Spell):
    name: str = "Poison"
    mana_cost: int = 173
    duration: int = 6
    damage: int = 3


@dataclass
class Recharge(Spell):
    name: str = "Recharge"
    mana_cost: int = 229
    duration: int = 5
    recharge: int = 101


def _make_spells() -> List[Spell]:
    spells = [
        MagicMissile(),
        Drain(),
        Shield(),
        Poison(),
        Recharge(),
    ]
    return {spell.name: spell for spell in spells}


M = "Magic Missile"
D = "Drain"
P = "Poison"
S = "Shield"
R = "Recharge"


def _spell_order():

    for spell_name in [P, R, S, M, M, M, R, P, S]:
        yield spell_name
    while True:
        yield M


@dataclass
class Character:
    name: str
    max_hitpoints: int
    base_damage: int = 0
    base_armor: int = 0
    max_mana: int = 500
    mana_spent: int = 0
    current_hp: int = field(init=False)
    current_mana: int = field(init=False)
    spell_order: List[str] = field(default_factory=_spell_order)
    # spell_order: Generator = field(init=False)
    spells: Dict[str, Spell] = field(default_factory=_make_spells)

    def __post_init__(self):
        self.current_hp = self.max_hitpoints
        self.current_mana = self.max_mana

    @property
    def damage(self):
        return self.base_damage

    @property
    def armor(self):
        shield = self.get_spell("Shield")
        modifier = shield.shield if shield.timer > 0 else 0
        return self.base_armor + modifier

    def take_damage(self, amount: int) -> int:
        self.current_hp = max(0, self.current_hp - amount)
        return self.current_hp

    def heal(self, amount: int) -> int:
        self.current_hp += amount
        return self.current_hp

    def recharge(self, amount: int) -> int:
        self.current_mana += amount
        return self.current_mana

    def attack(self, other: Character) -> int:
        dmg_dealt = max(1, self.damage - other.armor)
        other.current_hp = other.take_damage(dmg_dealt)
        return other.current_hp

    def resolve_effects(self, other: Character):
        for spell_name in self.spells:
            spell = self.spells[spell_name]
            if spell.timer > 0:
                spell.resolve_effect(self, other)

    def get_spell(self, spell_name: str) -> Spell:
        return self.spells[spell_name]

    def can_cast(self, spell_name: str) -> bool:
        spell = self.get_spell(spell_name)
        return self.current_mana >= spell.mana_cost and spell.timer == 0

    # def spell_order(self):
    #     # for spell_name in _spell_order():
    #     ...

    def determine_spell(self, other: Character) -> Spell:
        for spell_name in self.spell_order:
            if self.can_cast(spell_name):
                return self.get_spell(spell_name)
            else:
                raise ValueError(f"Can't cast {spell_name}")

        return self.get_spell(next(self.spell_order))

        if (
            self.can_cast("Magic Missile")
            and other.current_hp <= self.get_spell("Magic Missile").damage
        ):
            return self.get_spell("Magic Missile")

        if self.can_cast("Recharge"):
            return self.get_spell("Recharge")

        if self.can_cast("Poison"):
            return self.get_spell("Poison")

        if self.can_cast("Shield"):
            return self.get_spell("Shield")

        return self.get_spell("Magic Missile")

    def cast(self, other: Character):
        spell = self.determine_spell(other)
        return spell.cast(self, other)

    @classmethod
    def make_player(cls):
        return cls(**PLAYER_STATS)

    @classmethod
    def make_boss(cls):
        return cls(**BOSS_STATS)


def battle(player: Character, boss: Character):
    winner = None
    while player.current_hp > 0 and boss.current_hp > 0:
        player.resolve_effects(boss)
        player.cast(boss)
        if boss.current_hp <= 0:
            return player

        boss.attack(player)
        if player.current_hp <= 0:
            return boss

        print(player.name, player.current_hp, player.mana_spent)
        print(boss.name, boss.current_hp, boss.mana_spent)


def part_one(_: str) -> int:
    player = Character.make_player()
    boss = Character.make_boss()
    winner = battle(player, boss)
    print(f"The winner is {winner.name} and they spent {winner.mana_spent}.")
    return winner.mana_spent


def part_two(_: str) -> int:
    return -1


def solve(func: Callable[[str], int]):
    input_file = ""
    result = func(input_file)
    print(f"The solution for {func.__name__!r} is {result}")


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
    print(Poison.mana_cost + 10 * MagicMissile.mana_cost + Recharge.mana_cost)
