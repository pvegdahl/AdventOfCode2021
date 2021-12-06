from collections import defaultdict
from typing import Dict

import pytest


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("", {}),
        ("1", {1: 1}),
        ("1,1", {1: 2}),
        ("1,1,2", {1: 2, 2: 1}),
        ("1,1,2, 3, 4, 2, 1, 4, 6, 0", {1: 3, 2: 2, 3: 1, 4: 2, 6: 1, 0: 1}),
    ],
)
def test_parse_input(input_string, expected):
    assert parse_input(input_string) == expected


def parse_input(input_string) -> Dict[int, int]:
    if not input_string:
        return {}
    numbers = [int(num_string) for num_string in input_string.split(",")]
    result = defaultdict(lambda: 0)
    for number in numbers:
        result[number] += 1
    return result


def day6a(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


def day6b(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    print(f"The answer to 6A is: {day6a('../puzzle_input/day6.txt')}")
    print(f"The answer to 6B is: {day6b('../puzzle_input/day6.txt')}")
