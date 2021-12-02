from collections import defaultdict
from typing import Tuple, List, Dict

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


@pytest.mark.parametrize("vector_list, expected", [
    ([], {}),
    ([("down", 5)], {"down": 5}),
    ([("up", 3), ("down", 5)], {"down": 5, "up": 3}),
    ([("up", 3), ("down", 5), ("down", 6)], {"down": 11, "up": 3}),
])
def test_sum_by_type(vector_list, expected):
    assert sum_by_type(vector_list) == expected


def sum_by_type(vector_list: List[Tuple[str, int]]) -> Dict[str, int]:
    result = defaultdict(lambda: 0)
    for vector in vector_list:
        result[vector[0]] += vector[1]
    return result


