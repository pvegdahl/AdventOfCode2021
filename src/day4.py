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
        ("1, 2\n\n1 2 3 2 1\n 3 4 5 6 7\n 1 2 3 4 5\n 9 8 7 6 5\n 63 64 65 66 67", [[[1, 2, 3, 2, 1], [3, 4, 5, 6, 7], [1, 2, 3, 4, 5], [9, 8, 7, 6, 5], [63, 64, 65, 66, 67]]]),
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
            matrix.append([int(number) for number in line.strip().split(" ")])
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


@pytest.mark.parametrize("matrix, rows, columns, remaining", [
    ([[1]], [{1}], [{1}], [1]),
    ([[1, 2], [3, 4]], [{1, 2}, {3, 4}], [{1, 3}, {2, 4}], [1, 2, 3, 4]),
])
def test_bingo_board_creation(matrix, rows, columns, remaining):
    bingo_board = BingoBoard(matrix)
    assert bingo_board.rows == rows
    assert bingo_board.columns == columns
    assert bingo_board.remaining == remaining


@pytest.mark.parametrize("bingo_board, updates, rows, columns, remaining", [
    (BingoBoard([[1]]), [1], [set()], [set()], []),
    (BingoBoard([[1, 2], [3, 4]]), [1], [{2}, {3, 4}], [{3}, {2, 4}], [2, 3, 4]),
    (BingoBoard([[1, 2], [3, 4]]), [1, 4], [{2}, {3}], [{3}, {2}], [2, 3]),
    (BingoBoard([[1, 2], [3, 4]]), [1, 2], [set(), {3, 4}], [{3}, {4}], [3, 4]),
])
def test_bingo_call_number(bingo_board, updates, rows, columns, remaining):
    for number in updates:
        bingo_board.call_number(number)
    assert bingo_board.rows == rows
    assert bingo_board.columns == columns
    assert bingo_board.remaining == remaining


def day4a(filepath: str):
    with open(filepath, "r") as file:
        # parsed_input = parse_input(filepath)
        pass


def day4b(filepath: str):
    with open(filepath, "r") as file:
        # parsed_input = parse_input(filepath)
        pass


if __name__ == "__main__":
    print(f"The answer to 4A is: {day4a('../puzzle_input/day4.txt')}")
    print("**********")
    print(f"The answer to 4B is: {day4b('../puzzle_input/day4.txt')}")
