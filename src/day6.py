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


@pytest.mark.parametrize(
    "initial_state, expected",
    [
        ({}, {}),
        ({1: 1}, {0: 1}),
        ({1: 1, 2: 2, 3: 3}, {0: 1, 1: 2, 2: 3}),
        ({0: 1}, {6: 1, 8: 1}),
        ({1: 1, 2: 2, 3: 3, 0: 43}, {0: 1, 1: 2, 2: 3, 6: 43, 8: 43}),
        ({0: 2, 7: 2}, {6: 4, 8: 2}),
    ],
)
def test_one_day_change(initial_state, expected):
    assert one_day_change(initial_state) == expected


def one_day_change(initial_state: Dict[int, int]) -> Dict[int, int]:
    result = defaultdict(lambda: 0)
    for key, value in initial_state.items():
        if key == 0:
            result[6] += initial_state[0]
            result[8] += initial_state[0]
        else:
            result[key - 1] += value
    return result


@pytest.mark.parametrize(
    "initial_state, days, expected",
    [
        ({}, 1, {}),
        ({1: 1}, 1, {0: 1}),
        ({1: 1, 2: 2, 3: 3}, 1, {0: 1, 1: 2, 2: 3}),
        ({0: 1}, 1, {6: 1, 8: 1}),
        ({1: 1, 2: 2, 3: 3, 0: 43}, 1, {0: 1, 1: 2, 2: 3, 6: 43, 8: 43}),
        ({1: 1}, 2, {6: 1, 8: 1}),
        ({1: 1}, 4, {4: 1, 6: 1}),
        ({0: 1, 2: 2}, 4, {3: 1, 5: 3, 7: 2}),
    ],
)
def test_n_day_change(initial_state, days, expected):
    assert n_day_change(initial_state=initial_state, days=days) == expected


def n_day_change(initial_state: Dict[int, int], days: int) -> Dict[int, int]:
    result = initial_state
    for _ in range(days):
        result = one_day_change(result)
    return result


def day6a(filepath: str) -> int:
    with open(filepath, "r") as file:
        initial_state = parse_input(file.read())
    final_state = n_day_change(initial_state=initial_state, days=80)
    return sum(final_state.values())


def day6b(filepath: str) -> int:
    with open(filepath, "r") as file:
        initial_state = parse_input(file.read())
    final_state = n_day_change(initial_state=initial_state, days=256)
    return sum(final_state.values())


if __name__ == "__main__":
    print(f"The answer to 6A is: {day6a('../puzzle_input/day6.txt')}")
    print(f"The answer to 6B is: {day6b('../puzzle_input/day6.txt')}")
