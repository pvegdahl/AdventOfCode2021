from typing import List

import pytest


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("", []),
        ("1", [1]),
        ("1,2,3,4,5,4,3,2,1", [1, 2, 3, 4, 5, 4, 3, 2, 1]),
    ],
)
def test_parse_input(input_string, expected):
    assert parse_input(input_string) == expected


def parse_input(input_string) -> List[int]:
    if not input_string:
        return []
    return [int(number) for number in input_string.strip().split(",")]


def day7a(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


def day7b(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    print(f"The answer to 7A is: {day7a('../puzzle_input/day7.txt')}")
    print(f"The answer to 7B is: {day7b('../puzzle_input/day7.txt')}")
