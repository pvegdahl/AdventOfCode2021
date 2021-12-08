from collections import defaultdict
from collections import defaultdict
from typing import List, Dict

import pytest


@pytest.mark.parametrize(
    "input_line, expected",
    [
        ("abc dfe ihg | anything it does not matter", ["abc", "def", "ghi"]),
        (
            "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | whatever",
            [
                "abcdefg",
                "bcdef",
                "acdfg",
                "abcdf",
                "abd",
                "abcdef",
                "bcdefg",
                "abef",
                "abcdeg",
                "ab",
            ],
        ),
    ],
)
def test_parse_one_line_of_input_signal_patterns(input_line, expected):
    assert parse_one_line_of_input_signal_patterns(input_line) == expected


def parse_one_line_of_input_signal_patterns(input_line) -> List[str]:
    result_unsorted = input_line.split("|")[0].strip().split(" ")
    return ["".join(sorted(value)) for value in result_unsorted]


@pytest.mark.parametrize(
    "input_line, expected",
    [
        ("abc def ghi | some other string", ["emos", "ehort", "ginrst"]),
    ],
)
def test_parse_one_line_of_output_signal_patterns(input_line, expected):
    assert parse_one_line_of_output_signal_patterns(input_line) == expected


def parse_one_line_of_output_signal_patterns(input_line) -> List[str]:
    result_unsorted = input_line.split("|")[1].strip().split(" ")
    return ["".join(sorted(value)) for value in result_unsorted]


@pytest.mark.parametrize(
    "patterns, expected",
    [
        (
            ["a", "ab", "abc", "abcd", "abcde", "abcdef", "def", "dcba", "xyz"],
            {1: 1, 2: 1, 3: 3, 4: 2, 5: 1, 6: 1},
        )
    ],
)
def test_count_by_lengths(patterns, expected):
    assert count_by_lengths(patterns) == expected


def count_by_lengths(patterns: List[str]) -> Dict[int, int]:
    result = defaultdict(lambda: 0)
    for pattern in patterns:
        result[len(pattern)] += 1
    return result


@pytest.mark.parametrize(
    "input_patterns, expected",
    [
        (
            [
                "acedgfb",
                "cdfbe",
                "gcdfa",
                "fbcad",
                "dab",
                "cefabd",
                "cdfgeb",
                "eafb",
                "cagedb",
                "ab",
            ],
            {
                "abcdefg": 8,
                "bcdef": 5,
                "acdfg": 2,
                "abcdf": 3,
                "abd": 7,
                "abcdef": 9,
                "bcdefg": 6,
                "abef": 4,
                "abcdeg": 0,
                "ab": 1,
            },
        )
    ],
)
def test_decode_patterns(input_patterns, expected):
    assert decode_patterns(input_patterns) == expected


@pytest.mark.parametrize(
    "input_patterns, expected",
    [
        (
            [
                "acedgfb",
                "cdfbe",
                "gcdfa",
                "fbcad",
                "dab",
                "cefabd",
                "cdfgeb",
                "eafb",
                "cagedb",
                "ab",
            ],
            {
                "A": "a",
                "B": "a",
                "C": "a",
                "D": "a",
                "E": "a",
                "F": "a",
                "G": "a",
            },
        )
    ],
)
def decode_patterns(input_patterns: List[str]) -> Dict:
    sorted_patterns = ["".join(sorted(pattern)) for pattern in input_patterns]


def test_decode_letter_mapping():
    pass


def day8a(filepath: str) -> int:
    output_patterns = []
    with open(filepath, "r") as file:
        for line in file.readlines():
            output_patterns += parse_one_line_of_output_signal_patterns(line)
    counts = count_by_lengths(output_patterns)
    return counts[2] + counts[4] + counts[3] + counts[7]


def day8b(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    print(f"The answer to 8A is: {day8a('../puzzle_input/day8.txt')}")
    print(f"The answer to 8B is: {day8b('../puzzle_input/day8.txt')}")
