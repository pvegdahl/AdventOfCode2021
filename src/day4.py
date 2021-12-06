from statistics import mode
from typing import Tuple, List, Callable

import pytest


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("", []),
        ("1", [1]),
        ("1, 2", [1, 2]),
        ("3, 1, 4, 1, 5", [3, 1, 4, 1, 5]),
        ("1, 2\n\n1 2 3", [1, 2]),
    ],
)
def test_parse_bingo_numbers(input_string, expected):
    assert parse_bingo_numbers(input_string) == expected


def parse_bingo_numbers(input_string: str) -> List[int]:
    if not input_string:
        return []

    return [int(number) for number in input_string.split("\n")[0].split(",")]


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("", []),
        ("1", []),
        ("1, 2", []),
        ("3, 1, 4, 1, 5", []),
        ("1\n\n4", [[[4]]]),
        ("1, 2\n\n1 2\n 3 4", [[[1, 2], [3, 4]]]),
        ("1, 2\n\n1  2\n 3    4", [[[1, 2], [3, 4]]]),
        (
            "1, 2\n\n1 2 3 2 1\n 3 4 5 6 7\n 1 2 3 4 5\n 9 8 7 6 5\n 63 64 65 66 67",
            [
                [
                    [1, 2, 3, 2, 1],
                    [3, 4, 5, 6, 7],
                    [1, 2, 3, 4, 5],
                    [9, 8, 7, 6, 5],
                    [63, 64, 65, 66, 67],
                ]
            ],
        ),
        ("1\n\n4\n", [[[4]]]),
        ("1\n\n4\n\n3\n\n2\n\n1\n", [[[4]], [[3]], [[2]], [[1]]]),
    ],
)
def test_parse_bingo_boards_to_matrices(input_string, expected):
    assert parse_bingo_boards_to_matrices(input_string) == expected


def parse_bingo_boards_to_matrices(input_string: str) -> List[List[List[int]]]:
    split_on_lines = input_string.split("\n")
    result = []
    matrix = []
    for line in split_on_lines[2:]:
        if line:
            matrix.append([int(number) for number in line.strip().split()])
        else:
            result.append(matrix)
            matrix = []
    if matrix:
        result.append(matrix)
    return result


class BingoBoard:
    def __init__(self, matrix: List[List[int]]):
        self.rows = self.calc_rows(matrix)
        self.columns = self.calc_columns(matrix)
        self.remaining = self.calc_all(matrix)

    @staticmethod
    def calc_rows(matrix: List[List[int]]):
        return [set(row) for row in matrix]

    @staticmethod
    def calc_columns(matrix: List[List[int]]):
        return [set([row[i] for row in matrix]) for i in range(len(matrix[0]))]

    @staticmethod
    def calc_all(matrix):
        result = []
        for row in matrix:
            result.extend(row)
        return result

    def call_number(self, number: int):
        for row in self.rows:
            row.discard(number)
        for column in self.columns:
            column.discard(number)
        self.remaining = [x for x in self.remaining if x != number]

    def is_win(self):
        return any([len(x) == 0 for x in (self.rows + self.columns)])

    def score(self, multiplier: int) -> int:
        return sum(self.remaining) * multiplier


@pytest.mark.parametrize(
    "matrix, rows, columns, remaining",
    [
        ([[1]], [{1}], [{1}], [1]),
        ([[1, 2], [3, 4]], [{1, 2}, {3, 4}], [{1, 3}, {2, 4}], [1, 2, 3, 4]),
    ],
)
def test_bingo_board_creation(matrix, rows, columns, remaining):
    bingo_board = BingoBoard(matrix)
    assert bingo_board.rows == rows
    assert bingo_board.columns == columns
    assert bingo_board.remaining == remaining


@pytest.mark.parametrize(
    "bingo_board, updates, rows, columns, remaining",
    [
        (BingoBoard([[1]]), [1], [set()], [set()], []),
        (BingoBoard([[1, 2], [3, 4]]), [1], [{2}, {3, 4}], [{3}, {2, 4}], [2, 3, 4]),
        (BingoBoard([[1, 2], [3, 4]]), [1, 4], [{2}, {3}], [{3}, {2}], [2, 3]),
        (BingoBoard([[1, 2], [3, 4]]), [1, 2], [set(), {3, 4}], [{3}, {4}], [3, 4]),
    ],
)
def test_bingo_call_number(bingo_board, updates, rows, columns, remaining):
    for number in updates:
        bingo_board.call_number(number)
    assert bingo_board.rows == rows
    assert bingo_board.columns == columns
    assert bingo_board.remaining == remaining


@pytest.mark.parametrize(
    "bingo_board, updates, expected",
    [
        (BingoBoard([[1]]), [], False),
        (BingoBoard([[1]]), [2, 3, 4], False),
        (BingoBoard([[1]]), [2, 3, 4, 1], True),
        (BingoBoard([[1, 2], [3, 4]]), [1], False),
        (BingoBoard([[1, 2], [3, 4]]), [1, 2], True),
        (BingoBoard([[1, 2], [3, 4]]), [1, 3], True),
        (BingoBoard([[1, 2], [3, 4]]), [1, 4], False),
    ],
)
def test_is_win(bingo_board, updates, expected):
    for number in updates:
        bingo_board.call_number(number)
    assert bingo_board.is_win() == expected


@pytest.mark.parametrize(
    "bingo_board, updates, multiplier, expected",
    [
        (BingoBoard([[1]]), [], 1, 1),
        (BingoBoard([[1]]), [2, 3, 4], 4, 4),
        (BingoBoard([[1]]), [2, 3, 4, 1], 23456, 0),
        (BingoBoard([[1, 2], [3, 4]]), [1], 2, 18),
        (BingoBoard([[1, 2], [3, 4]]), [1, 2], 3, 21),
        (BingoBoard([[1, 2], [3, 4]]), [1, 3], 5, 30),
        (BingoBoard([[1, 2], [3, 4]]), [1, 4], 4, 20),
    ],
)
def test_board_score(bingo_board, updates, multiplier, expected):
    for number in updates:
        bingo_board.call_number(number)
    assert bingo_board.score(multiplier) == expected


def day4a(filepath: str):
    with open(filepath, "r") as file:
        input_string = file.read()
    bingo_numbers = parse_bingo_numbers(input_string)
    bingo_boards = [
        BingoBoard(matrix) for matrix in parse_bingo_boards_to_matrices(input_string)
    ]
    for number in bingo_numbers:
        for board in bingo_boards:
            board.call_number(number)
            if board.is_win():
                return board.score(multiplier=number)


def day4b(filepath: str):
    with open(filepath, "r") as file:
        input_string = file.read()
    bingo_numbers = parse_bingo_numbers(input_string)
    bingo_boards = [
        BingoBoard(matrix) for matrix in parse_bingo_boards_to_matrices(input_string)
    ]
    winning_boards = 0
    for number in bingo_numbers:
        for board in bingo_boards:
            if not board.is_win():
                board.call_number(number)
                if board.is_win():
                    winning_boards += 1
                    if winning_boards == len(bingo_boards):
                        return board.score(multiplier=number)


if __name__ == "__main__":
    print(f"The answer to 4A is: {day4a('../puzzle_input/day4.txt')}")
    print("**********")
    print(f"The answer to 4B is: {day4b('../puzzle_input/day4.txt')}")
