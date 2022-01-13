"""
Advent of Code 2015: Day 4
"""

import hashlib

SECRET_KEY = "ckczppom"


def hash_number(number: int):
    value = SECRET_KEY + str(number)
    encoded = value.encode()
    hashed_value = hashlib.md5(encoded)
    return hashed_value.hexdigest()


def check_hash(hashed: str, zeroes: int):
    return hashed[:zeroes] == "0" * zeroes

def solve(zeroes):
    number = 1
    while not check_hash(hash_number(number), zeroes):
        number += 1
    print(number)

def main():
    solve(5)
    solve(6)


if __name__ == "__main__":
    main()
