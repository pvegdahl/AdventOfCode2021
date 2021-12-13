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
        (
            {"start": {"a", "b"}, "a": {"end"}, "b": {"end"}},
            {("start", "a", "end"), ("start", "b", "end")},
        ),
        (
            {"start": {"a", "b"}, "a": {"c", "end"}, "b": {"end"}, "c": {"a"}},
            {("start", "a", "end"), ("start", "b", "end")},
        ),
        (
            {"start": {"a", "b"}, "a": {"c", "end"}, "b": {"end"}, "c": {"a", "end"}},
            {("start", "a", "c", "end"), ("start", "a", "end"), ("start", "b", "end")},
        ),
        (
            {"start": {"A", "b"}, "A": {"c", "end"}, "b": {"end"}, "c": {"A"}},
            {
                ("start", "A", "c", "A", "end"),
                ("start", "A", "end"),
                ("start", "b", "end"),
            },
        ),
    ],
)
def test_find_paths(cave_map, expected):
    assert find_paths(cave_map) == expected


@pytest.mark.parametrize(
    "input_text, expected_count",
    [
        (
            """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""",
            19,
        ),
        (
            """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""",
            226,
        ),
    ],
)
def test_find_paths_aoc(input_text, expected_count):
    assert len(find_paths(parse_input(input_text))) == expected_count


def find_paths(cave_map: Dict[str, Set[str]]) -> Set[Tuple[str, ...]]:
    return find_paths_recursive(cave_map=cave_map, current_path=("start",))


def find_paths_recursive(
    cave_map: Dict[str, Set[str]], current_path: Tuple[str, ...]
) -> Set[Tuple[str, ...]]:
    current_position = current_path[-1]
    if current_position == "end":
        return {current_path}

    results = set()
    for cave in cave_map[current_position]:
        if can_visit_cave(cave=cave, current_path=current_path):
            results.update(
                find_paths_recursive(
                    cave_map=cave_map, current_path=(current_path + (cave,))
                )
            )
    return results


def can_visit_cave(cave: str, current_path: Tuple[str, ...]):
    return is_uppercase(cave) or cave not in current_path


def is_uppercase(text: str) -> bool:
    return text == text.upper()


def part_a(filepath: str):
    with open(filepath, "r") as file:
        return len(find_paths(parse_input(file.read())))


def part_b(filepath: str):
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    day = 12
    input_file = f"../puzzle_input/day{day}.txt"
    print(f"The answer to {day}A is: {part_a(input_file)}")
    print(f"The answer to {day}B is: {part_b(input_file)}")
