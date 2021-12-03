from collections import defaultdict
from typing import Tuple, List, Dict, NamedTuple

import pytest


@pytest.mark.parametrize(
    "input_string, expected_list",
    [
        ("", [()]),
        ("1", [(1,)]),
        ("0", [(0,)]),
        ("11", [(1, 1)]),
        ("00", [(0, 0)]),
        ("010111", [(0, 1, 0, 1, 1, 1)]),
        ("11\n00", [(1, 1), (0, 0)]),
        (
            "010111\n111111\n000000\n000111",
            [
                (0, 1, 0, 1, 1, 1),
                (1, 1, 1, 1, 1, 1),
                (0, 0, 0, 0, 0, 0),
                (0, 0, 0, 1, 1, 1),
            ],
        ),
    ],
)
def test_parse_input(input_string, expected_list):
    assert parse_input(input_string) == expected_list


def parse_input(input_string: str) -> List[Tuple[int]]:
    result = []
    for line in input_string.strip().split("\n"):
        result.append(tuple(int(char) for char in line.strip()))
    return result


def day3a(filepath: str):
    with open(filepath, "r") as file:
        pass


def day3b(filepath: str):
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    print(f"The answer to 3A is: {day3a('../puzzle_input/day3.txt')}")
    print(f"The answer to 3B is: {day3b('../puzzle_input/day3.txt')}")
