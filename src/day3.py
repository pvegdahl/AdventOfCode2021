from statistics import mode
from typing import Tuple, List, Callable

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
    column = tuple(row[position] for row in binary_input)
    return mode_with_tiebreaker(column)


def least_common_bit_with_tiebreaker(data: List[Tuple[int]], position: int) -> int:
    return 1 - most_common_bit(binary_input=data, position=position)


@pytest.mark.parametrize(
    "data, tiebreaker, expected",
    [
        ((0,), 1, 0),
        ((1,), 1, 1),
        ((1,), 0, 1),
        ((1, 1), 1, 1),
        ((1, 1), 0, 1),
        ((1, 0), 1, 1),
        ((1, 0), 1, 1),
        ((0, 1), 1, 1),
        ((1, 0), 0, 0),
        ((0, 1), 0, 0),
        ((0, 0), 1, 0),
    ],
)
def test_mode_with_tiebreaker(data, tiebreaker, expected):
    assert mode_with_tiebreaker(data, tiebreaker) == expected


def mode_with_tiebreaker(data: Tuple[int], tiebreaker: int = 1) -> int:
    other = 1 - tiebreaker
    return mode((tiebreaker, other) + data)


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
    "most_common_bits, expected",
    [
        ((0,), 1),
        ((1,), 0),
        ((1, 1), 0),
        ((0, 0), 3),
        ((1, 0, 1, 1, 0), 9),
        ((0, 1, 0, 0, 1), 22),
    ],
)
def test_epsilon_rate(most_common_bits, expected):
    assert epsilon_rate(most_common_bits) == expected


def epsilon_rate(most_common_bits):
    least_common_bits = tuple(1 - bit for bit in most_common_bits)
    return binary_to_int(least_common_bits)


@pytest.mark.parametrize(
    "data, position, expected",
    [
        ([(1,)], 0, [(1,)]),
        ([(1, 0), (1, 1)], 0, [(1, 0), (1, 1)]),
        ([(1, 0), (1, 1), (0, 1)], 0, [(1, 0), (1, 1)]),
        ([(0, 1), (1, 0), (1, 1)], 0, [(1, 0), (1, 1)]),
        ([(0, 1), (1, 0), (1, 1)], 1, [(0, 1), (1, 1)]),
        ([(0, 1), (1, 1), (0, 0)], 0, [(0, 1), (0, 0)]),
        ([(1, 1), (1, 0), (0, 1), (0, 0)], 0, [(1, 1), (1, 0)]),
        ([(1, 1), (1, 0), (0, 1), (0, 0)], 1, [(1, 1), (0, 1)]),
    ],
)
def test_oxygen_filter(data, position, expected):
    assert oxygen_filter(data, position) == expected


def oxygen_filter(data, position):
    filter_bit = most_common_bit(binary_input=data, position=position)
    return [value for value in data if value[position] == filter_bit]


@pytest.mark.parametrize(
    "data, expected",
    [
        ([(1, 0)], (1, 0)),
        ([(1, 0), (1, 1)], (1, 1)),
        ([(1, 1), (1, 0)], (1, 1)),
        (
            [
                (0, 0, 1, 0, 0),
                (1, 1, 1, 1, 0),
                (1, 0, 1, 1, 0),
                (1, 0, 1, 1, 1),
                (1, 0, 1, 0, 1),
                (0, 1, 1, 1, 1),
                (0, 0, 1, 1, 1),
                (1, 1, 1, 0, 0),
                (1, 0, 0, 0, 0),
                (1, 1, 0, 0, 1),
                (0, 0, 0, 1, 0),
                (0, 1, 0, 1, 0),
            ],
            (1, 0, 1, 1, 1),
        ),
    ],
)
def test_filter_to_one(data, expected):
    assert filter_to_one(data, oxygen_filter) == expected


def filter_to_one(
    data: List[Tuple[int]], a_filter: Callable = oxygen_filter
) -> Tuple[int]:
    position = 0
    while len(data) > 1:
        data = a_filter(data=data, position=position)
        position += 1
    return data[0]


@pytest.mark.parametrize(
    "data, position, expected",
    [
        ([(1,)], 0, []),
        ([(1, 0), (1, 1)], 0, []),
        ([(1, 0), (1, 1)], 1, [(1, 0)]),
        ([(1, 0), (1, 1), (0, 0)], 0, [(0, 0)]),
    ],
)
def test_co2_filter(data, position, expected):
    assert co2_filter(data, position) == expected


def test_co2_filter_to_one():
    data = [
        (0, 0, 1, 0, 0),
        (1, 1, 1, 1, 0),
        (1, 0, 1, 1, 0),
        (1, 0, 1, 1, 1),
        (1, 0, 1, 0, 1),
        (0, 1, 1, 1, 1),
        (0, 0, 1, 1, 1),
        (1, 1, 1, 0, 0),
        (1, 0, 0, 0, 0),
        (1, 1, 0, 0, 1),
        (0, 0, 0, 1, 0),
        (0, 1, 0, 1, 0),
    ]
    expected = (0, 1, 0, 1, 0)
    assert filter_to_one(data=data, a_filter=co2_filter) == expected


def co2_filter(data, position):
    filter_bit = least_common_bit_with_tiebreaker(data=data, position=position)
    return [value for value in data if value[position] == filter_bit]


def day3a(filepath: str):
    with open(filepath, "r") as file:
        binary_input_data = parse_input(file.read())
    most_common_bits = most_common_bit_list(binary_input_data)
    print(f"gamma = {gamma_rate(most_common_bits)}")
    print(f"epsilon = {epsilon_rate(most_common_bits)}")
    print(
        f"gamma+epsilon = {gamma_rate(most_common_bits) + epsilon_rate(most_common_bits)}"
    )
    return gamma_rate(most_common_bits) * epsilon_rate(most_common_bits)


def day3b(filepath: str):
    with open(filepath, "r") as file:
        binary_input_data = parse_input(file.read())
    oxygen_value = binary_to_int(
        filter_to_one(data=binary_input_data, a_filter=oxygen_filter)
    )
    co2_value = binary_to_int(
        filter_to_one(data=binary_input_data, a_filter=co2_filter)
    )
    print(f"oxygen = {oxygen_value}")
    print(f"co2 = {co2_value}")
    return oxygen_value * co2_value


if __name__ == "__main__":
    print(f"The answer to 3A is: {day3a('../puzzle_input/day3.txt')}")
    print("**********")
    print(f"The answer to 3B is: {day3b('../puzzle_input/day3.txt')}")
