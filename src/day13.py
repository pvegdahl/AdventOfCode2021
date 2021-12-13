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
        [dimension, coordinate] = input_string.strip()[11:].split("=")
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
    "points, a_fold, expected",
    [
        (set(), Fold("x", 3), set()),
        ({Point(0, 0)}, Fold("x", 3), {Point(0, 0)}),
        (
            {Point(0, 0), Point(1, 1), Point(2, 2)},
            Fold("x", 3),
            {Point(0, 0), Point(1, 1), Point(2, 2)},
        ),
        ({Point(0, 0), Point(2, 0)}, Fold("x", 1), {Point(0, 0)}),
        ({Point(0, 0), Point(3, 0)}, Fold("x", 2), {Point(0, 0), Point(1, 0)}),
        (
            {Point(1, 0), Point(4, 0), Point(5, 1), Point(6, 2)},
            Fold("x", 3),
            {Point(1, 0), Point(2, 0), Point(1, 1), Point(0, 2)},
        ),
        (
                {Point(0, 1), Point(0, 4), Point(1, 5), Point(2, 6)},
                Fold("y", 3),
                {Point(0, 1), Point(0, 2), Point(1, 1), Point(2, 0)},
        ),
    ],
)
def test_fold(points, a_fold, expected):
    assert fold(points=points, a_fold=a_fold) == expected


@pytest.fixture()
def aoc_input_text() -> str:
    return """6,10
    0,14
    9,10
    0,3
    10,4
    4,11
    6,0
    6,12
    4,1
    0,13
    10,12
    3,4
    3,0
    8,4
    1,10
    2,14
    8,10
    9,0

    fold along y=7
    fold along x=5"""


def test_fold_aoc_example(aoc_input_text):
    points = parse_input_points(aoc_input_text)
    folds = parse_input_folds(aoc_input_text)
    for a_fold in folds:
        points = fold(points=points, a_fold=a_fold)
    assert points == {
        Point(0, 0),
        Point(1, 0),
        Point(2, 0),
        Point(3, 0),
        Point(4, 0),
        Point(0, 1),
        Point(0, 2),
        Point(0, 3),
        Point(0, 4),
        Point(4, 1),
        Point(4, 2),
        Point(4, 3),
        Point(4, 4),
        Point(1, 4),
        Point(2, 4),
        Point(3, 4),
    }


def fold(points: Set[Point], a_fold: Fold) -> Set[Point]:
    if a_fold.dimension == "x":
        return fold_on_x(a_fold, points)
    elif a_fold.dimension == "y":
        return fold_on_y(a_fold, points)
    else:
        raise Exception(f"Cannot fold on {a_fold.dimension}")


def fold_on_x(a_fold, points):
    kept_points = {point for point in points if point.x < a_fold.coordinate}
    folded_points = {
        Point(x=(2 * a_fold.coordinate - point.x), y=point.y)
        for point in points
        if point.x > a_fold.coordinate
    }
    return kept_points.union(folded_points)


def fold_on_y(a_fold, points):
    kept_points = {point for point in points if point.y < a_fold.coordinate}
    folded_points = {
        Point(x=point.x, y=(2 * a_fold.coordinate - point.y))
        for point in points
        if point.y > a_fold.coordinate
    }
    return kept_points.union(folded_points)


def part_a(filepath: str):
    with open(filepath, "r") as file:
        input_text = file.read()
    points = parse_input_points(input_text)
    a_fold = parse_input_folds(input_text)[0]
    return len(fold(points=points, a_fold=a_fold))


def part_b(filepath: str):
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    day = 13
    input_file = f"../puzzle_input/day{day}.txt"
    print(f"The answer to {day}A is: {part_a(input_file)}")
    print(f"The answer to {day}B is: {part_b(input_file)}")
