from typing import List, NamedTuple

import pytest


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_string(cls, input_string: str) -> "Point":
        [x, y] = [int(a) for a in input_string.split(",")]
        return cls(x, y)


class LineSegment(NamedTuple):
    start: Point
    end: Point
    x0: int = 0
    y0: int = 0
    x1: int = 0
    y1: int = 0

    @classmethod
    def from_string(cls, input_string: str) -> "LineSegment":
        points = input_string.split(" -> ")
        start = Point.from_string(points[0])
        end = Point.from_string(points[1])
        return cls(start, end)

    def get_points(self):
        result = {self.start, self.end}
        [first, last] = sorted([self.start.y, self.end.y])
        for y in range(first, last):
            result.add(Point(self.start.x, y))
        return result


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("", []),
        ("0,0 -> 0,1", [LineSegment(start=Point(0, 0), end=Point(0, 1))]),
        ("1,2 -> 3,4", [LineSegment(start=Point(1, 2), end=Point(3, 4))]),
        ("1,2 -> 3,4\n5,6 -> 7,8\n", [LineSegment(start=Point(1, 2), end=Point(3, 4)), LineSegment(start=Point(5, 6), end=Point(7, 8))]),
        ],
)
def test_parse_input(input_string, expected):
    assert parse_input(input_string) == expected


def parse_input(input_string) -> List[LineSegment]:
    result = []
    for line in input_string.split("\n"):
        if line:
            result.append(LineSegment.from_string(line))
    return result


@pytest.mark.parametrize(
    "line_segment, expected",
    [
        (LineSegment(start=Point(0, 0), end=Point(0, 0)), {Point(0, 0)}),
        (LineSegment(start=Point(0, 0), end=Point(0, 1)), {Point(0, 0), Point(0, 1)}),
        (LineSegment(start=Point(0, 0), end=Point(0, 3)), {Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)}),
        (LineSegment(start=Point(0, 3), end=Point(0, 0)), {Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)}),
    ],
)
def test_get_points_on_line_segment(line_segment, expected):
    assert line_segment.get_points() == expected


def day5a(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


def day5b(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    print(f"The answer to 5A is: {day5a('../puzzle_input/day5.txt')}")
    print(f"The answer to 5B is: {day2a('../puzzle_input/day5.txt')}")
