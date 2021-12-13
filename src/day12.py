from collections import defaultdict
from typing import Set, Dict, Tuple

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


def parse_input(input_string) -> Dict[str, Set[str]]:
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


@pytest.mark.parametrize(
    "cave_map, expected",
    [
        ({"start": {"end"}}, {("start", "end")}),
        ({"start": {"a"}, "a": {"end"}}, {("start", "a", "end")}),
        ({"start": {"a"}, "a": {"b"}, "b": {"end"}}, {("start", "a", "b", "end")}),
        ({"start": {"a", "b"}, "a": {"end"}, "b": {"end"}}, {("start", "a", "end"), ("start", "b", "end")}),
        # ({"start": {"a", "b"}, "a": {"c", "end"}, "b": {"end"}, "c": {"a"}}, {("start", "a", "end"), ("start", "b", "end")}),
    ],
)
def test_find_paths(cave_map, expected):
    assert find_paths(cave_map) == expected


def find_paths(cave_map: Dict[str, Set[str]]) -> Set[Tuple[str, ...]]:
    return find_paths_recursive(cave_map=cave_map, current_path=("start",))


def find_paths_recursive(cave_map: Dict[str, Set[str]], current_path: Tuple[str, ...]) -> Set[Tuple[str, ...]]:
    current_position = current_path[-1]
    if current_position == "end":
        return {current_path}

    results = set()
    for option in cave_map[current_position]:
        results.update(find_paths_recursive(cave_map=cave_map, current_path=(current_path + (option,))))
    return results


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
