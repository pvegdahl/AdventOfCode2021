from typing import Optional, List, Any

import pytest


@pytest.mark.parametrize(
    "input_string, expected",
    [
    ],
)
def test_parse_input(input_string, expected):
    assert parse_input(input_string) == expected


def parse_input(input_string):
    pass


def day11a(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


def day11b(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    print(f"The answer to 11A is: {day11a('../puzzle_input/day11.txt')}")
    print(f"The answer to 11B is: {day11b('../puzzle_input/day11.txt')}")
