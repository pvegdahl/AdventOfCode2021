import functools
from collections import defaultdict
from statistics import mean
from typing import List, Tuple, Callable, Dict

import pytest


@pytest.mark.parametrize(
    "input_line, expected",
    [
        ("abc def ghi | anything it does not matter", ["abc", "def", "ghi"])
    ],
)
def test_parse_one_line_of_input_signal_patterns(input_line, expected):
    assert parse_one_line_of_input_signal_patterns(input_line) == expected


def parse_one_line_of_input_signal_patterns(input_line) -> List[str]:
    return input_line.split("|")[0].strip().split(" ")


@pytest.mark.parametrize(
    "input_line, expected",
    [
        ("abc def ghi | some other strings", ["some", "other", "strings"])
    ],
)
def test_parse_one_line_of_output_signal_patterns(input_line, expected):
    assert parse_one_line_of_output_signal_patterns(input_line) == expected


def parse_one_line_of_output_signal_patterns(input_line) -> List[str]:
    return input_line.split("|")[1].strip().split(" ")


@pytest.mark.parametrize(
    "input_patterns, expected",
    [
        (["a", "ab", "abc", "abcd", "abcde", "abcdef", "def", "dcba", "xyz"], {1: 1, 2: 1, 3: 3, 4: 2, 5: 1, 6: 1})
    ],
)
def test_count_by_lengths(input_patterns, expected):
    assert count_by_lengths(input_patterns) == expected


def count_by_lengths(input_patterns: List[str]) -> Dict[int, int]:
    result = defaultdict(lambda: 0)
    for pattern in input_patterns:
        result[len(pattern)] += 1
    return result


def day8a(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


def day8b(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    print(f"The answer to 8A is: {day8a('../puzzle_input/day8.txt')}")
    print(f"The answer to 8B is: {day8b('../puzzle_input/day8.txt')}")
