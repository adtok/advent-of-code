"""Advent of Code 2015: Day 10"""

from typing import Callable


CONFUSING_LETTERS = ["i", "l", "o"]


def increment_password(password: str) -> str:
    new_password = ""
    carry = False
    for i, char in enumerate(password[::-1]):
        if i == 0 or carry:
            new_char = increment_letter(char)
            if new_char in CONFUSING_LETTERS:
                new_char = increment_letter(new_char)
            new_password = new_char + new_password
            carry = False
            if new_char == "a":
                carry = True
        else:
            new_password = char + new_password

    if carry:
        new_password = "a" + new_password

    print(new_password)
    return new_password


def increment_letter(letter: str) -> str:
    val = ord(letter)
    assert 97 <= val <= 122
    new_val = (val - 96) % 26 + 1
    return chr(new_val + 96)


def check_password(password: str) -> bool:
    return (
        consecutive_increasing(password) >= 3
        and not confusing_letters(password)
        and unique_pairs(password) >= 2
    )


def consecutive_increasing(password: str) -> bool:
    longest = 1
    current = 1
    for i, char in enumerate(password[1:]):
        if char != "a" and char == increment_letter(password[i]):
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    return longest


def confusing_letters(password: str) -> bool:
    return any(letter in password for letter in CONFUSING_LETTERS)


def unique_pairs(password: str) -> int:
    return sum(password.count(c * 2) > 0 for c in set(password))


def solve(func: Callable[[str], str]):
    input_value = "vzbxkghb"
    result = func(input_value)
    print(f"The solution for {func.__name__!r} is {result!r}")


def part_one(input_value: str) -> str:
    password = input_value
    while not check_password(password):
        password = increment_password(password)
    return password


def part_two(input_value: str) -> str:
    password = part_one(input_value)
    password = increment_password(password)
    password = part_one(password)
    return password


def main():
    solve(part_one)
    solve(part_two)


if __name__ == "__main__":
    main()
