from typing import List, Tuple

import pytest


@pytest.fixture()
def test_matrix():
    return [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def test_parse_input(test_matrix):
    assert parse_input("123\n456\n789") == test_matrix


def parse_input(input_string):
    if not input_string:
        return []
    result = []
    for line in input_string.strip().split("\n"):
        result.append([int(char) for char in line.strip()])
    return result


def test_add_one_to_everything(test_matrix):
    assert add_one_to_everything(test_matrix) == [[2, 3, 4], [5, 6, 7], [8, 9, 10]]
    assert test_matrix != add_one_to_everything(test_matrix)  # Do not mutate the input


def add_one_to_everything(matrix: List[List[int]]) -> List[List[int]]:
    result = []
    for row in matrix:
        result.append([x + 1 for x in row])
    return result


@pytest.mark.parametrize("threshold, expected", [
    (300, []),
    (9, []),
    (8, [(2, 2)]),
    (4, [(1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]),
])
def test_find_cells_greater_than_threshold(threshold, expected, test_matrix):
    assert sorted(find_cells_greater_than_threshold(matrix=test_matrix, threshold=threshold)) == sorted(expected)


def find_cells_greater_than_threshold(matrix: List[List[int]], threshold: int = 9) -> List[Tuple[int, int]]:
    result = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > threshold:
                result.append((i, j))
    return result


def day11a(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


def day11b(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    print(f"The answer to 11A is: {day11a('../puzzle_input/day11.txt')}")
    print(f"The answer to 11B is: {day11b('../puzzle_input/day11.txt')}")
