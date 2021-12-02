from collections import defaultdict
from typing import Tuple, List, Dict, NamedTuple

import pytest


@pytest.mark.parametrize("input_string, expected_list", [
    ("", []),
    ("forward 5", [("forward", 5)]),
    ("up 2", [("up", 2)]),
    ("down 123", [("down", 123)]),
    ("forward 5\nup 2\ndown 123", [("forward", 5), ("up", 2), ("down", 123)]),
    ("forward 5\nup 2\ndown 123\n", [("forward", 5), ("up", 2), ("down", 123)]),
])
def test_parse_input(input_string, expected_list):
    assert parse_input(input_string) == expected_list


def parse_input(input_string: str) -> List[Tuple[str, int]]:
    if not input_string:
        return []
    result = []
    for line in input_string.strip().split("\n"):
        line_split = line.split(" ")
        result.append((line_split[0], int(line_split[1])))
    return result


@pytest.mark.parametrize("vector_list, expected", [
    ([], {}),
    ([("down", 5)], {"down": 5}),
    ([("up", 3), ("down", 5)], {"down": 5, "up": 3}),
    ([("up", 3), ("down", 5), ("down", 6)], {"down": 11, "up": 3}),
])
def test_sum_by_type(vector_list, expected):
    assert sum_by_type(vector_list) == expected


def sum_by_type(vector_list: List[Tuple[str, int]]) -> Dict[str, int]:
    result = defaultdict(lambda: 0)
    for vector in vector_list:
        result[vector[0]] += vector[1]
    return result


@pytest.mark.parametrize("direction_sums, expected", [
    ({}, 0),
    ({"forward": 86}, 0),
    ({"down": 86}, 86),
    ({"up": 4}, -4),
    ({"down": 99, "up": 86}, 13),
])
def test_calculate_depth(direction_sums, expected):
    assert calculate_depth(direction_sums) == expected


def calculate_depth(direction_sums: Dict[str, int]) -> int:
    return (direction_sums.get("down") or 0) - (direction_sums.get("up") or 0)


@pytest.mark.parametrize("initial_aim, vector, expected_aim", [
    (0, ("down", 0), 0),
    (3, ("down", 0), 3),
    (0, ("down", 5), 5),
    (3, ("down", 5), 8),
    (3, ("forward", 5), 3),
    (3, ("up", 1), 2),
])
def test_adjust_aim(initial_aim: int, vector: Tuple[str, int], expected_aim: int):
    assert adjust_aim(initial_aim, vector) == expected_aim


def adjust_aim(initial_aim: int, vector: Tuple[str, int]) -> int:
    if vector[0] == "down":
        return initial_aim + vector[1]
    elif vector[0] == "up":
        return initial_aim - vector[1]
    return initial_aim


class SubmarineState(NamedTuple):
    horizontal: int = 0
    depth: int = 0
    aim: int = 0


@pytest.mark.parametrize("initial_state, vector, expected_state", [
    (SubmarineState(), ("down", 0), SubmarineState()),
    (SubmarineState(1, 2, 3), ("down", 0), SubmarineState(1, 2, 3)),
    (SubmarineState(), ("forward", 6), SubmarineState(6, 0, 0)),
    (SubmarineState(), ("down", 3), SubmarineState(0, 0, 3)),
])
def test_update_submarine_state(initial_state, vector, expected_state):
    assert update_submarine_state(initial_state, vector) == expected_state


def update_submarine_state(initial_state: SubmarineState, vector: Tuple[str, int]) -> SubmarineState:
    horizontal_adjustment = 0
    depth_adjustment = 0
    aim_adjustment = 0
    if vector[0] == "forward":
        horizontal_adjustment = vector[1]
    if vector[0] == "down":
        aim_adjustment = vector[1]
    return SubmarineState(
        horizontal=initial_state.horizontal + horizontal_adjustment,
        depth=initial_state.depth + depth_adjustment,
        aim=initial_state.aim + aim_adjustment
    )


def day_2a(filepath: str) :
    with open(filepath, "r") as file:
        vector_list = parse_input(file.read())
    direction_by_type = sum_by_type(vector_list)
    horizontal = direction_by_type.get("forward") or 0
    depth = calculate_depth(direction_by_type)
    print(f"Horizontal = {horizontal}, Depth = {depth}")
    return horizontal * depth


if __name__ == "__main__":
    print(f"The answer to 2A is: {day_2a('../puzzle_input/day2.txt')}")
