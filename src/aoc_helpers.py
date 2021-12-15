from typing import NamedTuple, List, Any, Tuple

import pytest


@pytest.mark.parametrize(
    "text, expected",
    [
        ("123\n456\n789", [[1, 4, 7], [2, 5, 8], [3, 6, 9]]),
        ("123\n456", [[1, 4], [2, 5], [3, 6]]),
    ],
)
def test_parse_digit_matrix(text, expected):
    assert parse_digit_matrix(text) == expected


def parse_digit_matrix(input_string: str) -> List[List[int]]:
    if not input_string:
        return []
    result_transposed = []
    for line in input_string.strip().split("\n"):
        result_transposed.append([int(char) for char in line.strip()])
    result = [[0] * len(result_transposed) for _ in result_transposed[0]]
    for x in range(len(result)):
        for y in range(len(result[0])):
            result[x][y] = result_transposed[y][x]
    return result


@pytest.mark.parametrize(
    "list_matrix, expected",
    [
        ([[1, 4, 7], [2, 5, 8], [3, 6, 9]], ((1, 4, 7), (2, 5, 8), (3, 6, 9))),
        ([[1, 4], [2, 5], [3, 6]], ((1, 4), (2, 5), (3, 6))),
    ],
)
def test_list_matrix_to_tuple_matrix(list_matrix, expected):
    assert list_matrix_to_tuple_matrix(list_matrix) == expected


def list_matrix_to_tuple_matrix(
    list_matrix: List[List[Any]],
) -> Tuple[Tuple[Any, ...], ...]:
    return tuple(tuple(row) for row in list_matrix)


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_string(cls, input_string: str) -> "Point":
        [x, y] = [int(a) for a in input_string.split(",")]
        return cls(x, y)
