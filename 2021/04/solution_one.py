"""
Advent of Code 2021: Day 04 Part 1
tldr: Bingo
"""


from typing import List, Set


def parse_board(board: str) -> List[int]:
    lines = list(map(int, board.split()))
    assert len(lines) == len(set(lines))
    return lines


def check_board(board: List[int], drew: Set[int]) -> bool:
    for i in range(5):
        row_i = board[5 * i : 5 * i + 5]
        col_i = board[i::5]
        if all(val in drew for val in row_i) or all(val in drew for val in col_i):
            return True
    return False


def score_board(board: List[int], drew: Set[int], last_drawn: int) -> int:
    result = (sum(board) - sum(d for d in drew if d in board)) * last_drawn
    return result


def solve(input_file: str) -> int:
    with open(input_file, "r") as file:
        draws, *boards = file.read().split("\n\n")

    draws = list(map(int, draws.split(",")))
    boards = list(map(parse_board, boards))
    drew = set()

    for draw in draws:
        drew.add(draw)
        for board in boards:
            if check_board(board, drew):
                result = score_board(board, drew, draw)
                print(f"The solution to {input_file!r} is {result}.")
                return result

    print(f"Could not find a solution for {input_file!r}.")
    return -1


def main():
    test_result = solve("input.test")
    test_answer = 4512
    assert test_result == test_answer
    solve("input.solution")


if __name__ == "__main__":
    main()
