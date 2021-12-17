import math
from typing import NamedTuple, Tuple, Optional, List, Set

import pytest

from src.aoc_helpers import Point


class TargetArea(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def is_inside(self, point: Point) -> bool:
        return (
            self.min_x <= point.x <= self.max_x and self.min_y <= point.y <= self.max_y
        )


MY_AOC_TARGET_AREA_INPUT = TargetArea(min_x=282, max_x=314, min_y=-80, max_y=-45)


@pytest.mark.parametrize(
    "target_area, point, expected",
    [
        (TargetArea(0, 5, 0, 5), Point(1, 1), True),
        (TargetArea(0, 5, 0, 5), Point(6, 1), False),
        (TargetArea(0, 5, 0, 5), Point(-1, 1), False),
        (TargetArea(0, 5, 0, 5), Point(0, 1), True),
        (TargetArea(0, 5, 0, 5), Point(5, 1), True),
        (TargetArea(0, 5, 0, 5), Point(1, -1), False),
        (TargetArea(0, 5, 0, 5), Point(1, 0), True),
        (TargetArea(0, 5, 0, 5), Point(1, 8), False),
        (TargetArea(0, 5, 0, 5), Point(1, 5), True),
    ],
)
def test_target_area_is_inside(target_area: TargetArea, point, expected):
    assert target_area.is_inside(point) == expected


class Velocity(NamedTuple):
    x: int
    y: int

    def one_step(self) -> "Velocity":
        if self.x >= 0:
            return Velocity(max(self.x - 1, 0), self.y - 1)
        else:
            return Velocity(self.x + 1, self.y - 1)


@pytest.mark.parametrize(
    "velocity, expected",
    [
        (Velocity(0, 0), Velocity(0, -1)),
        (Velocity(0, 10), Velocity(0, 9)),
        (Velocity(0, -10), Velocity(0, -11)),
        (Velocity(10, 10), Velocity(9, 9)),
        (Velocity(-10, 10), Velocity(-9, 9)),
    ],
)
def test_velocity_one_step(velocity, expected):
    assert velocity.one_step() == expected


def find_x_step_range(target_area: TargetArea) -> Optional[Tuple[int, int]]:
    speed_for_min = math.ceil(initial_speed_for_final_x_position(target_area.min_x))
    speed_for_max = math.floor(initial_speed_for_final_x_position(target_area.max_x))
    if speed_for_max < speed_for_min:
        return None
    return speed_for_min, speed_for_max


def initial_speed_for_final_x_position(final_position) -> float:
    return (-1 + math.sqrt(1 + 8 * final_position)) / 2


@pytest.mark.parametrize(
    "target_area, expected",
    [
        (TargetArea(1, 1, 1, 1), (1, 1)),
        (TargetArea(1, 2, 1, 1), (1, 1)),
        (TargetArea(1, 3, 1, 1), (1, 2)),
        (TargetArea(2, 2, 1, 1), None),
    ],
)
def test_find_x_step_range(target_area, expected):
    assert find_x_step_range(target_area) == expected


def falls_in_target(target_area: TargetArea, velocity: Velocity) -> bool:
    current_position = Point(0, 0)
    current_velocity = velocity
    while current_position.y >= target_area.min_y or current_velocity.y > 0:
        if target_area.is_inside(current_position):
            return True
        current_position = Point(
            x=current_position.x + current_velocity.x,
            y=current_position.y + current_velocity.y,
        )
        current_velocity = current_velocity.one_step()
    return False


def brute_force_find_possible_velocities(target_area: TargetArea) -> Set[Velocity]:
    min_x = 1
    max_x = target_area.max_x
    min_y = target_area.min_y
    max_y = 100
    results = set()
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            velocity = Velocity(x, y)
            if falls_in_target(target_area=target_area, velocity=velocity):
                results.add(velocity)
    return results


@pytest.mark.parametrize(
    "target_area, expected_subset",
    [
        (
            TargetArea(20, 30, -10, -5),
            {Velocity(7, 2), Velocity(6, 3), Velocity(9, 0), Velocity(6, 9)},
        )
    ],
)
def test_brute_force_find_possible_velocities(target_area, expected_subset):
    assert expected_subset.issubset(brute_force_find_possible_velocities(target_area))


def find_max_height(target_area: TargetArea) -> int:
    possible_velocities = brute_force_find_possible_velocities(target_area)
    max_y_velocity = max([v.y for v in possible_velocities])
    return int(max_y_velocity * (max_y_velocity + 1) / 2)


@pytest.mark.parametrize(
    "target_area, expected",
    [
        (TargetArea(20, 30, -10, -5), 45),
    ],
)
def test_find_max_height(target_area, expected):
    assert find_max_height(target_area) == expected


def part_a():
    return find_max_height(MY_AOC_TARGET_AREA_INPUT)


def part_b():
    return len(brute_force_find_possible_velocities(MY_AOC_TARGET_AREA_INPUT))


if __name__ == "__main__":
    day = 17
    input_file = f"../puzzle_input/day{day}.txt"
    print(f"The answer to {day}A is: {part_a()}")
    print(f"The answer to {day}B is: {part_b()}")
