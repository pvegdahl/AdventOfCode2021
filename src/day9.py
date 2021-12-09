from typing import List

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


def day9a(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


def day9b(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    print(f"The answer to 9A is: {day9a('../puzzle_input/day9.txt')}")
    print(f"The answer to 9B is: {day9b('../puzzle_input/day9.txt')}")
