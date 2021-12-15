from typing import NamedTuple


def test_parse_digit_matrix():
    assert parse_digit_matrix("123\n456\n789") == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    assert parse_digit_matrix("123\n456") == [[1, 4], [2, 5], [3, 6]]


def parse_digit_matrix(input_string):
    if not input_string:
        return []
    result_transposed = []
    for line in input_string.strip().split("\n"):
        result_transposed.append([int(char) for char in line.strip()])
    result = [[None] * len(result_transposed) for _ in result_transposed[0]]
    for x in range(len(result)):
        for y in range(len(result[0])):
            result[x][y] = result_transposed[y][x]
    return result


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_string(cls, input_string: str) -> "Point":
        [x, y] = [int(a) for a in input_string.split(",")]
        return cls(x, y)
