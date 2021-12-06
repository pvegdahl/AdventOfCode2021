from collections import defaultdict
from typing import List, NamedTuple, Set, Dict, Optional

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

    @classmethod
    def from_string(cls, input_string: str) -> "LineSegment":
        points = input_string.split(" -> ")
        start = Point.from_string(points[0])
        end = Point.from_string(points[1])
        return cls(start, end)

    def get_points(self, consider_diagonals: Optional[bool] = False) -> Set[Point]:
        result = set()
        if self.start.x == self.end.x:
            [first, last] = sorted([self.start.y, self.end.y])
            for y in range(first, last + 1):
                result.add(Point(self.start.x, y))
        elif self.start.y == self.end.y:
            [first, last] = sorted([self.start.x, self.end.x])
            for x in range(first, last + 1):
                result.add(Point(x, self.start.y))
        elif consider_diagonals:
            if self.start.x < self.end.x:
                first_x = self.start.x
                last_x = self.end.x
                first_y = self.start.y
                last_y = self.end.y
            else:
                first_x = self.end.x
                last_x = self.start.x
                first_y = self.end.y
                last_y = self.start.y

            if first_y < last_y:
                slope = 1
            else:
                slope = -1

            for i in range(0, last_x - first_x + 1):
                result.add(Point(first_x + i, first_y + slope * i))
        return result


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("", []),
        ("0,0 -> 0,1", [LineSegment(start=Point(0, 0), end=Point(0, 1))]),
        ("1,2 -> 3,4", [LineSegment(start=Point(1, 2), end=Point(3, 4))]),
        (
            "1,2 -> 3,4\n5,6 -> 7,8\n",
            [
                LineSegment(start=Point(1, 2), end=Point(3, 4)),
                LineSegment(start=Point(5, 6), end=Point(7, 8)),
            ],
        ),
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
        (
            LineSegment(start=Point(0, 0), end=Point(0, 3)),
            {Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)},
        ),
        (
            LineSegment(start=Point(0, 3), end=Point(0, 0)),
            {Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)},
        ),
        (
            LineSegment(start=Point(5, 6), end=Point(7, 6)),
            {Point(5, 6), Point(6, 6), Point(7, 6)},
        ),
        (
            LineSegment(start=Point(345, 678), end=Point(342, 678)),
            {
                Point(342, 678),
                Point(343, 678),
                Point(344, 678),
                Point(345, 678),
            },
        ),
        (LineSegment(start=Point(1, 2), end=Point(3, 4)), set()),
    ],
)
def test_get_points_on_line_segment_no_diagonals(line_segment, expected):
    assert line_segment.get_points(consider_diagonals=False) == expected


@pytest.mark.parametrize(
    "line_segment, expected",
    [
        (
            LineSegment(start=Point(5, 6), end=Point(7, 6)),
            {Point(5, 6), Point(6, 6), Point(7, 6)},
        ),
        (
            LineSegment(start=Point(1, 1), end=Point(3, 3)),
            {Point(1, 1), Point(2, 2), Point(3, 3)},
        ),
        (
            LineSegment(start=Point(3, 3), end=Point(1, 1)),
            {Point(1, 1), Point(2, 2), Point(3, 3)},
        ),
        (
            LineSegment(start=Point(1, 3), end=Point(3, 1)),
            {Point(1, 3), Point(2, 2), Point(3, 1)},
        ),
        (
            LineSegment(start=Point(3, 1), end=Point(1, 3)),
            {Point(1, 3), Point(2, 2), Point(3, 1)},
        ),
    ],
)
def test_get_points_on_line_segment_with_diagonals(line_segment, expected):
    assert line_segment.get_points(consider_diagonals=True) == expected


@pytest.mark.parametrize(
    "line_segments, expected",
    [
        (
            [LineSegment(start=Point(0, 0), end=Point(0, 3))],
            {Point(0, 0): 1, Point(0, 1): 1, Point(0, 2): 1, Point(0, 3): 1},
        ),
        (
            [
                LineSegment(start=Point(0, 0), end=Point(0, 3)),
                LineSegment(start=Point(0, 0), end=Point(0, 3)),
            ],
            {Point(0, 0): 2, Point(0, 1): 2, Point(0, 2): 2, Point(0, 3): 2},
        ),
        (
            [
                LineSegment(start=Point(0, 0), end=Point(0, 3)),
                LineSegment(start=Point(0, 0), end=Point(0, 1)),
            ],
            {Point(0, 0): 2, Point(0, 1): 2, Point(0, 2): 1, Point(0, 3): 1},
        ),
        (
            [
                LineSegment(start=Point(0, 0), end=Point(0, 3)),
                LineSegment(start=Point(2, 2), end=Point(-1, 2)),
            ],
            {
                Point(0, 0): 1,
                Point(0, 1): 1,
                Point(0, 2): 2,
                Point(0, 3): 1,
                Point(2, 2): 1,
                Point(1, 2): 1,
                Point(-1, 2): 1,
            },
        ),
    ],
)
def test_sum_points(line_segments, expected):
    assert sum_points(line_segments) == expected


def sum_points(
    line_segments, consider_diagonals: Optional[bool] = False
) -> Dict[Point, int]:
    result = defaultdict(lambda: 0)
    for line_segment in line_segments:
        for point in line_segment.get_points(consider_diagonals):
            result[point] += 1
    return result


@pytest.mark.parametrize(
    "line_segments, expected",
    [
        (
            [
                LineSegment(start=Point(0, 0), end=Point(0, 3)),
                LineSegment(start=Point(2, 2), end=Point(-1, 2)),
            ],
            {Point(0, 2)},
        ),
        (
            [
                LineSegment(start=Point(0, 0), end=Point(0, 3)),
                LineSegment(start=Point(0, 1), end=Point(0, 2)),
                LineSegment(start=Point(2, 2), end=Point(-1, 2)),
            ],
            {Point(0, 2), Point(0, 1)},
        ),
        (
            [
                LineSegment(start=Point(0, 0), end=Point(0, 3)),
                LineSegment(start=Point(0, 1), end=Point(0, 2)),
                LineSegment(start=Point(2, 2), end=Point(-1, 2)),
                LineSegment(start=Point(2, 2), end=Point(-1, 2)),
                LineSegment(start=Point(100, 101), end=Point(200, 101)),
                LineSegment(start=Point(-1, -1), end=Point(1, 1)),
            ],
            {Point(0, 2), Point(0, 1), Point(2, 2), Point(1, 2), Point(-1, 2)},
        ),
    ],
)
def test_filter_to_two_plus(line_segments, expected):
    assert filter_to_two_plus(line_segments) == expected


def filter_to_two_plus(
    line_segments, consider_diagonals: Optional[bool] = False
) -> Set[Point]:
    point_counts = sum_points(
        line_segments=line_segments, consider_diagonals=consider_diagonals
    )
    result = {point for point, count in point_counts.items() if count > 1}
    return result


def day5a(filepath: str) -> int:
    with open(filepath, "r") as file:
        input_string = file.read()
    return len(
        filter_to_two_plus(
            line_segments=parse_input(input_string), consider_diagonals=False
        )
    )


def day5b(filepath: str) -> int:
    with open(filepath, "r") as file:
        input_string = file.read()
    return len(
        filter_to_two_plus(
            line_segments=parse_input(input_string), consider_diagonals=True
        )
    )


if __name__ == "__main__":
    print(f"The answer to 5A is: {day5a('../puzzle_input/day5.txt')}")
    print(f"The answer to 5B is: {day5b('../puzzle_input/day5.txt')}")
