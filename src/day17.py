from typing import NamedTuple

import pytest

from src.aoc_helpers import Point


class TargetArea(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def is_inside(self, point: Point) -> bool:
        return self.min_x <= point.x <= self.max_x and self.min_y <= point.y <= self.max_y


@pytest.mark.parametrize("target_area, point, expected", [
    (TargetArea(0, 5, 0, 5), Point(1, 1), True),
    (TargetArea(0, 5, 0, 5), Point(6, 1), False),
    (TargetArea(0, 5, 0, 5), Point(-1, 1), False),
    (TargetArea(0, 5, 0, 5), Point(0, 1), True),
    (TargetArea(0, 5, 0, 5), Point(5, 1), True),
    (TargetArea(0, 5, 0, 5), Point(1, -1), False),
    (TargetArea(0, 5, 0, 5), Point(1, 0), True),
    (TargetArea(0, 5, 0, 5), Point(1, 8), False),
    (TargetArea(0, 5, 0, 5), Point(1, 5), True),
])
def test_target_area_is_inside(target_area: TargetArea, point, expected):
    assert target_area.is_inside(point) == expected


MY_AOC_INPUT = TargetArea(min_x=282, max_x=314, min_y=-80, max_y=-45)


def part_a():
    pass


def part_b():
    pass


if __name__ == "__main__":
    day = 17
    input_file = f"../puzzle_input/day{day}.txt"
    print(f"The answer to {day}A is: {part_a()}")
    print(f"The answer to {day}B is: {part_b()}")
