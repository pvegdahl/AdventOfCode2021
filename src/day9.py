from typing import List, Tuple

import pytest


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("", []),
        ("12", [[1, 2]]),
        ("12321", [[1, 2, 3, 2, 1]]),
        ("12\n", [[1, 2]]),
        ("12\n43", [[1, 2], [4, 3]]),
    ],
)
def test_parse_input(input_string, expected):
    assert parse_input(input_string) == expected


def parse_input(input_string: str) -> List[List[int]]:
    if not input_string:
        return []
    lines = input_string.strip().split("\n")
    result = []
    for line in lines:
        result.append([int(x) for x in line.strip()])
    return result


@pytest.mark.parametrize(
    "matrix, expected",
    [
        ([[1]], [1]),
        ([[1, 2]], [1]),
        ([[2, 1]], [1]),
        ([[1, 2, 1]], [1, 1]),
        ([[1, 3, 2]], [1, 2]),
        ([[1, 2], [2, 1]], [1, 1]),
    ],
)
def test_find_low_points(matrix, expected):
    assert find_low_points(matrix) == expected


def find_low_points(matrix):
    return [matrix[point[0]][point[1]] for point in find_low_point_indices(matrix)]


@pytest.mark.parametrize(
    "matrix, expected",
    [
        ([[1]], [(0, 0)]),
        ([[1, 2]], [(0, 0)]),
        ([[2, 1]], [(0, 1)]),
        ([[1, 2, 1]], [(0, 0), (0, 2)]),
        ([[1, 3, 2]], [(0, 0), (0, 2)]),
        ([[1, 2], [2, 1]], [(0, 0), (1, 1)]),
    ],
)
def test_find_low_point_indices(matrix, expected):
    assert find_low_point_indices(matrix) == expected


def find_low_point_indices(matrix: List[List[int]]) -> List[Tuple[int, int]]:
    result = []
    for i in range(len(matrix)):
        line = matrix[i]
        for j in range(len(line)):
            if less_than_neighbors(matrix, i, j):
                result.append((i, j))
    return result


def less_than_neighbors(matrix: List[List[int]], i: int, j: int) -> bool:
    neighbors = get_matrix_neighbors(matrix, i, j)
    if neighbors:
        return matrix[i][j] < min(get_matrix_neighbors(matrix, i, j))
    else:
        return True


@pytest.mark.parametrize(
    "matrix, i, j, expected",
    [
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 0, 0, [2, 4]),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 0, [1, 5, 7]),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 1, [2, 4, 6, 8]),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 2, [6, 8]),
    ],
)
def test_get_matrix_neighbors(matrix, i, j, expected):
    assert sorted(get_matrix_neighbors(matrix, i, j)) == expected


def get_matrix_neighbors(matrix: List[List[int]], i: int, j: int) -> List[int]:
    return [(matrix[point[0]][point[1]]) for point in get_matrix_neighbor_indices(matrix, i, j)]


def get_matrix_neighbor_indices(matrix: List[List[int]], i: int, j: int) -> List[Tuple[int, int]]:
    result = []
    points = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    for point in points:
        if in_matrix(matrix=matrix, i=point[0], j=point[1]):
            result.append((point[0], point[1]))
    return result


def in_matrix(matrix: List[List[int]], i: int, j: int) -> bool:
    return (i >= 0) and (j >= 0) and (i < len(matrix)) and (j < len(matrix[i]))


def day9a(filepath: str) -> int:
    with open(filepath, "r") as file:
        data = parse_input(file.read())
    low_points = find_low_points(data)
    return len(low_points) + sum(low_points)


def day9b(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    print(f"The answer to 9A is: {day9a('../puzzle_input/day9.txt')}")
    print(f"The answer to 9B is: {day9b('../puzzle_input/day9.txt')}")
