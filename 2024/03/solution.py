from functools import reduce
from typing import Generator

EXAMPLE = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def read_chars(filename: str) -> Generator[str, None, None]:
    with open(filename, "r") as file:
        while c := file.read(1):
            yield c


def parse_mults(
    application: Generator[str, None, None],
    only_mults: bool = True,
) -> Generator[tuple[int, int], None, None]:
    enabled = True
    curr = ""
    r_1 = None
    r_2 = None
    for c in application:
        match (curr, c, r_1, r_2):
            case (_, "m" | "d", _, _):
                curr = c
                r_1 = None
                r_2 = None
            case (
                ("m", "u", None, None)
                | ("mu", "l", None, None)
                | ("d", "o", _, _)
                | ("do", "(" | "n", _, _)
                | ("don", "'", _, _)
                | ("don'", "t", _, _)
                | ("don't", "(", _, _)
            ):
                curr += c
            case ("do(", ")", _, _):
                enabled = True
                curr = ""
                r_1 = None
                r_2 = None
            case ("don't(", ")", _, _):
                enabled = False
                curr = ""
                r_1 = None
                r_2 = None
            case ("mul", "(", None, None):
                r_1 = ""
            case ("mul", n, a, None) if n.isnumeric() and (a == "" or a.isnumeric()):
                r_1 += n
            case ("mul", ",", a, None) if a.isnumeric():
                r_2 = ""
            case (
                "mul",
                n,
                a,
                b,
            ) if n.isnumeric() and (b == "" or b.isnumeric()):
                r_2 += n
            case ("mul", ")", a, b) if a.isnumeric() and b.isnumeric():
                if enabled or only_mults:
                    yield (int(a), int(b))
                curr = ""
                r_1 = None
                r_2 = None
            case (current, _, _, _) if current:
                curr = ""
                r_1 = None
                r_2 = None
            case _:
                curr = ""
                r_1 = None
                r_2 = None


def part_one() -> int:
    chars = read_chars("input.txt")
    mults = parse_mults(chars)
    products = (a * b for a, b in mults)
    result = sum(products)
    return result


def part_two() -> int:
    chars = read_chars("input.txt")
    mults = parse_mults(chars, only_mults=False)
    products = (a * b for a, b in mults)
    result = sum(products)
    return result


def main() -> None:
    result = part_one()
    print(f"Part 1: {result}")
    result = part_two()
    print(f"Part 2: {result}")


if __name__ == "__main__":
    main()
