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


def decode_patterns(input_patterns: List[str]) -> Dict:
    sorted_patterns = ["".join(sorted(pattern)) for pattern in input_patterns]


@pytest.mark.parametrize(
    "input_patterns, expected",
    [
        (
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
                {
                    "A": "d",
                    "B": "e",
                    "C": "a",
                    "D": "f",
                    "E": "g",
                    "F": "b",
                    "G": "c",
                },
        )
    ],
)
def test_decode_letter_mapping(input_patterns, expected):
    assert decode_letter_mapping(input_patterns) == expected


def decode_letter_mapping(patterns: []) -> Dict[str, str]:
    all_letters = []
    for pattern in patterns:
        all_letters.extend(pattern)
    letter_histogram = defaultdict(lambda: 0)
    for letter in all_letters:
        letter_histogram[letter] += 1
    reversed_letter_histogram = defaultdict(lambda: set())
    for letter, count in letter_histogram.items():
        reversed_letter_histogram[count].add(letter)

    pattern_for_one = set([x for x in patterns if len(x) == 2][0])
    pattern_for_four = set([x for x in patterns if len(x) == 4][0])

    result = {
        "A": next(iter(reversed_letter_histogram[8].difference(pattern_for_one))),
        "B": next(iter(reversed_letter_histogram[6])),
        "C": next(iter(reversed_letter_histogram[8].intersection(pattern_for_one))),
        "D": next(iter(reversed_letter_histogram[7].intersection(pattern_for_four))),
        "E": next(iter(reversed_letter_histogram[4])),
        "F": next(iter(reversed_letter_histogram[9])),
        "G": next(iter(reversed_letter_histogram[7].difference(pattern_for_four))),
    }
    return result



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
