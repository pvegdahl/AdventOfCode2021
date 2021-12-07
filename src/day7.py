from statistics import mean
from typing import List, Tuple

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


@pytest.mark.parametrize(
    "positions, expected",
    [
        ([1], (1, 0)),
        ([1, 2, 3], (2, 2)),
        ([16, 1, 2, 0, 4, 2, 7, 1, 2, 14], (2, 37)),
    ],
)
def test_best_position_and_fuel(positions, expected):
    assert best_position_and_fuel(positions) == expected


def best_position_and_fuel(positions) -> Tuple[int, int]:
    min_pos = min(positions)
    max_pos = max(positions)
    best_position = None
    best_fuel = 1e100
    for pos in range(min_pos, max_pos + 1):
        fuel = calculate_fuel(current_positions=positions, target_position=pos)
        if fuel < best_fuel:
            best_position = pos
            best_fuel = fuel
    return best_position, best_fuel


@pytest.mark.parametrize(
    "current_positions, target_position, expected",
    [
        ([1], 1, 0),
        ([1, 2, 3], 2, 2),
        ([16, 1, 2, 0, 4, 2, 7, 1, 2, 14], 2, 37),
    ],
)
def test_calculate_fuel(current_positions, target_position, expected):
    assert calculate_fuel(current_positions, target_position) == expected


def calculate_fuel(current_positions: List[int], target_position: int) -> int:
    return sum([abs(pos - target_position) for pos in current_positions])


def day7a(filepath: str) -> int:
    with open(filepath, "r") as file:
        current_positions = parse_input(file.read())
    pos, fuel = best_position_and_fuel(current_positions)
    print(f"Best position and fuel: {pos} and {fuel}")
    return fuel


def day7b(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    print(f"The answer to 7A is: {day7a('../puzzle_input/day7.txt')}")
    print(f"The answer to 7B is: {day7b('../puzzle_input/day7.txt')}")
