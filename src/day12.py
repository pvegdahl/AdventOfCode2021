from collections import defaultdict

import pytest


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("", {}),
        ("A-B", {"A": {"B"}, "B": {"A"}}),
        ("AB-cd", {"AB": {"cd"}, "cd": {"AB"}}),
        ("A-B\nc-d", {"A": {"B"}, "B": {"A"}, "c": {"d"}, "d": {"c"}}),
        ("A-B\nc-B", {"A": {"B"}, "B": {"A", "c"}, "c": {"B"}}),
        ("start-B", {"start": {"B"}}),
        ("B-start", {"start": {"B"}}),
        ("A-end", {"A": {"end"}}),
        ("end-A", {"A": {"end"}}),
    ],
)
def test_parse_input(input_string, expected):
    assert parse_input(input_string) == expected


def parse_input(input_string):
    result = defaultdict(lambda: set())
    if not input_string:
        return result

    for line in input_string.strip().split("\n"):
        [location_a, location_b] = line.strip().split("-")
        if location_a != "end" and location_b != "start":
            result[location_a].add(location_b)
        if location_a != "start" and location_b != "end":
            result[location_b].add(location_a)
    return result


def part_a(filepath: str):
    with open(filepath, "r") as file:
        pass


def part_b(filepath: str):
    with open(filepath, "r") as file:
        pass


DAY = 12

if __name__ == "__main__":
    print(f"The answer to {DAY}A is: {part_a('../puzzle_input/day{DAY}.txt')}")
    print(f"The answer to {DAY}B is: {part_b('../puzzle_input/day{DAY}.txt')}")
