from typing import NamedTuple, Set, List

import pytest


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_string(cls, input_string: str) -> "Point":
        [x, y] = input_string.strip().split(",")
        return Point(x=int(x), y=int(y))


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("", set()),
        ("1, 2", {Point(1, 2)}),
        ("86,99", {Point(86, 99)}),
        ("1,2\n3,4\n5,6\n", {Point(1, 2), Point(3, 4), Point(5, 6)}),
        (
            "1,2\n3,4\n5,6\n\nfold along x=42\nfold along y=47",
            {Point(1, 2), Point(3, 4), Point(5, 6)},
        ),
    ],
)
def test_parse_input_points(input_string, expected):
    assert parse_input_points(input_string) == expected


def parse_input_points(input_string) -> Set[Point]:
    if not input_string:
        return set()

    result = set()
    for line in input_string.strip().split("\n\n")[0].split("\n"):
        result.add(Point.from_string(line))
    return result


class Fold(NamedTuple):
    dimension: str
    coordinate: int

    @classmethod
    def from_string(cls, input_string: str) -> "Fold":
        [dimension, coordinate] = input_string[11:].strip().split("=")
        return Fold(dimension=dimension, coordinate=int(coordinate))


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("", []),
        ("1,2\n\nfold along x=42", [Fold("x", 42)]),
        ("1,2\n\nfold along x=42\nfold along y=47", [Fold("x", 42), Fold("y", 47)]),
    ],
)
def test_parse_input_folds(input_string, expected):
    assert parse_input_folds(input_string) == expected


def parse_input_folds(input_string: str) -> List[Fold]:
    if not input_string:
        return []

    result = []
    for line in input_string.strip().split("\n\n")[1].split("\n"):
        result.append(Fold.from_string(line))
    return result


@pytest.mark.parametrize(
    "points, dimension, coordinate, expected",
    [
        (set(), "x", 3, set()),
        ({Point(0, 0)}, "x", 3, {Point(0, 0)}),
        (
            {Point(0, 0), Point(1, 1), Point(2, 2)},
            "x",
            3,
            {Point(0, 0), Point(1, 1), Point(2, 2)},
        ),
        ({Point(0, 0), Point(2, 0)}, "x", 1, {Point(0, 0)}),
        ({Point(0, 0), Point(3, 0)}, "x", 2, {Point(0, 0), Point(1, 0)}),
        (
            {Point(1, 0), Point(4, 0), Point(5, 1), Point(6, 2)},
            "x",
            3,
            {Point(1, 0), Point(2, 0), Point(1, 1), Point(0, 2)},
        ),
    ],
)
def test_fold(points, dimension, coordinate, expected):
    assert fold(points=points, dimension=dimension, coordinate=coordinate) == expected


def fold(points: Set[Point], dimension: str, coordinate: int) -> Set[Point]:
    kept_points = {point for point in points if point.x < coordinate}
    folded_points = {
        Point(x=(2 * coordinate - point.x), y=point.y)
        for point in points
        if point.x > coordinate
    }
    return kept_points.union(folded_points)


def part_a(filepath: str):
    with open(filepath, "r") as file:
        pass


def part_b(filepath: str):
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    day = 13
    input_file = f"../puzzle_input/day{day}.txt"
    print(f"The answer to {day}A is: {part_a(input_file)}")
    print(f"The answer to {day}B is: {part_b(input_file)}")
