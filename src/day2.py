from typing import Tuple, List

import pytest


@pytest.mark.parametrize("input_string, expected_list", [
    ("", []),
    ("forward 5", [("forward", 5)]),
    ("up 2", [("up", 2)]),
    ("down 123", [("down", 123)]),
    ("forward 5\nup 2\ndown 123", [("forward", 5), ("up", 2), ("down", 123)]),
    ("forward 5\nup 2\ndown 123\n", [("forward", 5), ("up", 2), ("down", 123)]),
])
def test_parse_input(input_string, expected_list):
    assert parse_input(input_string) == expected_list


def parse_input(input_string: str) -> List[Tuple[str, int]]:
    if not input_string:
        return []
    result = []
    for line in input_string.strip().split("\n"):
        line_split = line.split(" ")
        result.append((line_split[0], int(line_split[1])))
    return result


@pytest.mark.parametrize("vector_list, vector_type, expected", [
    ([], "down", 0),
    ([("down", 5)], "down", 5),
    ([("down", 5)], "up", 0),
])
def test_sum_type(vector_list, vector_type, expected):
    assert sum_type(vector_list, vector_type) == expected


def sum_type(vector_list: List[Tuple[str, int]], vector_type: str) -> int:
    if vector_list and vector_list[0][0] == vector_type:
        return vector_list[0][1]
    return 0
