from typing import List, Tuple, Set

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


def test_increment_everything(test_matrix):
    assert increment_everything(test_matrix) == [[2, 3, 4], [5, 6, 7], [8, 9, 10]]
    assert test_matrix != increment_everything(test_matrix)  # Do not mutate the input


def increment_everything(matrix: List[List[int]]) -> List[List[int]]:
    result = []
    for row in matrix:
        result.append([x + 1 for x in row])
    return result


@pytest.mark.parametrize(
    "threshold, expected",
    [
        (300, set()),
        (9, set()),
        (8, {(2, 2)}),
        (4, {(1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}),
    ],
)
def test_find_cells_greater_than_threshold(threshold, expected, test_matrix):
    assert find_cells_greater_than_threshold(matrix=test_matrix, threshold=threshold) == expected


def find_cells_greater_than_threshold(
    matrix: List[List[int]], threshold: int = 9
) -> Set[Tuple[int, int]]:
    result = set()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > threshold:
                result.add((i, j))
    return result


@pytest.mark.parametrize("target_cells, expected", [
    (set(), [[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
    ({(0, 0)}, [[2, 2, 3], [4, 5, 6], [7, 8, 9]]),
    ({(1, 0), (2, 1), (0, 2)}, [[1, 2, 4], [5, 5, 6], [7, 9, 9]]),
])
def test_increment_target_cells(target_cells, expected, test_matrix):
    assert increment_target_cells(matrix=test_matrix, target_cells=target_cells) == expected


def increment_target_cells(matrix: List[List[int]], target_cells: Set[Tuple[int, int]]) -> List[List[int]]:
    result = []
    for i in range(len(matrix)):
        new_row = []
        for j in range(len(matrix[i])):
            new_value = matrix[i][j]
            if (i, j) in target_cells:
                new_value += 1
            new_row.append(new_value)
        result.append(new_row)
    return result


@pytest.mark.parametrize("target_cells, expected", [
    (set(), [[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
    ({(0, 0)}, [[0, 2, 3], [4, 5, 6], [7, 8, 9]]),
    ({(1, 0), (2, 1), (0, 2)}, [[1, 2, 0], [0, 5, 6], [7, 0, 9]]),
])
def test_reset_target_cells(target_cells, expected, test_matrix):
    assert reset_target_cells(matrix=test_matrix, target_cells=target_cells) == expected


def reset_target_cells(matrix: List[List[int]], target_cells: Set[Tuple[int, int]]) -> List[List[int]]:
    result = []
    for i in range(len(matrix)):
        new_row = []
        for j in range(len(matrix[i])):
            new_value = matrix[i][j]
            if (i, j) in target_cells:
                new_value = 0
            new_row.append(new_value)
        result.append(new_row)
    return result

@pytest.mark.parametrize(
    "x, y, expected",
    [
        (1, 1, {(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)}),
        (0, 0, {(0, 1), (1, 0), (1, 1)}),
        (1, 0, {(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)}),
    ],
)
def test_find_neighbor_cells(x, y, expected, test_matrix):
    assert find_neighbor_cells(matrix=test_matrix, x=x, y=y) == expected


def find_neighbor_cells(
    matrix: List[List[int]], x: int, y: int
) -> Set[Tuple[int, int]]:
    result = set()
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if in_matrix(matrix=matrix, x=i, y=j):
                result.add((i, j))
    result.remove((x, y))
    return result


def in_matrix(matrix: List[List[int]], x: int, y: int) -> bool:
    return 0 <= x < len(matrix) and 0 <= y < len(matrix[x])


@pytest.mark.parametrize(
    "cycles, expected_matrix, expected_flash_count",
    [
        (0, [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 0),
        (1, [[2, 3, 4], [6, 8, 9], [9, 0, 0]], 2),
        (2, [[4, 6, 7], [9, 0, 0], [0, 4, 3]], 5),
    ],
)
def test_run_n_cycles(cycles, expected_matrix, expected_flash_count, test_matrix):
    assert run_n_cycles(matrix=test_matrix, cycles=cycles) == (expected_matrix, expected_flash_count)


def run_n_cycles(matrix: List[List[int]], cycles: int) -> Tuple[List[List[int]], int]:
    updated_matrix = matrix
    flash_count = 0
    for _ in range(cycles):
        updated_matrix, count = run_one_cycle(updated_matrix)
        flash_count += count
    return updated_matrix, flash_count


@pytest.mark.parametrize(
    "matrix, expected",
    [
        (
                [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 0)
         ),
        (
                [[0, 0, 0], [0, 9, 0], [0, 0, 0]],
                ([[2, 2, 2], [2, 0, 2], [2, 2, 2]], 1),
        ),
        (
                [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                ([[2, 3, 4], [6, 8, 9], [9, 0, 0]], 2)
        ),
    ],
)
def test_run_one_cycle(matrix, expected):
    assert run_one_cycle(matrix=matrix) == expected


def run_one_cycle(matrix: List[List[int]]) -> Tuple[List[List[int]], int]:
    updated_matrix = increment_everything(matrix)
    to_process = find_cells_greater_than_threshold(updated_matrix)
    flashed_cells = set()
    while to_process:
        flasher = to_process.pop()
        if flasher not in flashed_cells:
            flashed_cells.add(flasher)
            neighbors = find_neighbor_cells(matrix=matrix, x=flasher[0], y = flasher[1])
            updated_matrix = increment_target_cells(matrix=updated_matrix, target_cells=neighbors)
            to_process.update(find_cells_greater_than_threshold(updated_matrix))
    return reset_target_cells(matrix=updated_matrix, target_cells=flashed_cells), len(flashed_cells)


def day11a(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


def day11b(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    print(f"The answer to 11A is: {day11a('../puzzle_input/day11.txt')}")
    print(f"The answer to 11B is: {day11b('../puzzle_input/day11.txt')}")
