from collections import defaultdict
from statistics import mode
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
            "010111  \n   111111\n000000\n000111   \n",
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


@pytest.mark.parametrize(
    "binary_input, position, expected",
    [
        ([(1, 0, 1)], 0, 1),
        ([(1, 0, 1)], 1, 0),
        ([(1, 0, 1)], 2, 1),
        ([(1, 0, 1), (0, 0, 0), (0, 1, 0)], 0, 0),
        ([(1, 0, 1), (0, 0, 0), (0, 1, 0)], 1, 0),
        ([(1, 0, 1), (0, 0, 0), (0, 1, 0)], 2, 0),
    ],
)
def test_most_common_bit(binary_input, position, expected):
    assert most_common_bit(binary_input, position) == expected


def most_common_bit(binary_input: List[Tuple[int]], position: int) -> int:
    column = [row[position] for row in binary_input]
    return mode(column)


@pytest.mark.parametrize(
    "binary_input, expected",
    [
        ([], tuple()),
        ([(1, 0, 1)], (1, 0, 1)),
        ([(1, 0, 1), (1, 1, 1), (1, 1, 1)], (1, 1, 1)),
        ([(1, 0, 1), (1, 1, 0), (0, 1, 0)], (1, 1, 0)),
    ],
)
def test_most_common_bit_list(binary_input, expected):
    assert most_common_bit_list(binary_input) == expected


def most_common_bit_list(binary_input: List[Tuple[int]]) -> Tuple[int]:
    if binary_input:
        return tuple(
            most_common_bit(binary_input, position)
            for position in range(len(binary_input[0]))
        )
    return tuple()


@pytest.mark.parametrize(
    "binary_input, expected",
    [
        (tuple(), 0),
        ((0,), 0),
        ((1,), 1),
        ((1, 0), 2),
        ((1, 0, 1), 5),
        ((1, 0, 1, 1, 0), 22),
        ((0, 1, 0, 0, 1), 9),
    ],
)
def test_binary_to_int(binary_input, expected):
    assert binary_to_int(binary_input) == expected


def binary_to_int(binary_input):
    result = 0
    current_position_value = 1
    for bit in reversed(binary_input):
        result += current_position_value * bit
        current_position_value *= 2
    return result


def gamma_rate(most_common_bits: Tuple[int]) -> int:
    return binary_to_int(most_common_bits)


@pytest.mark.parametrize(
    "most_common_bits, expected", [
        ((0,), 1),
        ((1,), 0),
        ((1, 1), 0),
        ((0, 0), 3),
        ((1, 0, 1, 1, 0), 9),
        ((0, 1, 0, 0, 1), 22),
    ]
)
def test_epsilon_rate(most_common_bits, expected):
    assert epsilon_rate(most_common_bits) == expected


def epsilon_rate(most_common_bits):
    least_common_bits = tuple(1 - bit for bit in most_common_bits)
    return binary_to_int(least_common_bits)


def day3a(filepath: str):
    with open(filepath, "r") as file:
        binary_input_data = parse_input(file.read())
    most_common_bits = most_common_bit_list(binary_input_data)
    print(f"gamma = {gamma_rate(most_common_bits)}")
    print(f"epsilon = {epsilon_rate(most_common_bits)}")
    print(f"gamma+epsilon = {gamma_rate(most_common_bits) + epsilon_rate(most_common_bits)}")
    return gamma_rate(most_common_bits) * epsilon_rate(most_common_bits)


def day3b(filepath: str):
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    print(f"The answer to 3A is: {day3a('../puzzle_input/day3.txt')}")
    print(f"The answer to 3B is: {day3b('../puzzle_input/day3.txt')}")
