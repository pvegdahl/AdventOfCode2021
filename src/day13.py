from typing import NamedTuple, Set, List

import pytest


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_string(cls, input_string):
        [x, y] = input_string.strip().split(",")
        return Point(x=int(x), y=int(y))


@pytest.mark.parametrize("input_string, expected", [
    ("", set()),
    ("1, 2", {Point(1, 2)}),
    ("86,99", {Point(86, 99)}),
    ("1,2\n3,4\n5,6\n", {Point(1, 2), Point(3, 4), Point(5, 6)}),
    ("1,2\n3,4\n5,6\n\nfold along x=42\nfold along y=47", {Point(1, 2), Point(3, 4), Point(5, 6)}),
])
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


@pytest.mark.parametrize("input_string, expected", [
    ("", []),
    ])
def test_parse_input_folds(input_string, expected):
    assert parse_input_folds(input_string) == expected


def parse_input_folds(input_string: str) -> List[Fold]:
    return []



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
