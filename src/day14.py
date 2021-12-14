import pytest


@pytest.mark.parametrize("input_string, expected", [
    ("", ""),
    ("ABC", "ABC"),
    ("ABC\n", "ABC"),
    ("ABC\n\n", "ABC"),
    ("ABC\n\nAB -> C", "ABC"),
])
def test_parse_polymer_template(input_string, expected):
    assert parse_polymer_template(input_string) == expected


def parse_polymer_template(input_string: str) -> str:
    if not input_string:
        return ""
    return input_string.split("\n")[0].strip()


@pytest.mark.parametrize("input_string, expected", [
    ("", {}),
    ("ABC\n\n", {}),
    ("ABC\n\nAB -> C", {"AB": "C"}),
    ("ABC\n\nAB -> C\nCA -> B", {"AB": "C", "CA": "B"}),
])
def test_parse_insertion_rules(input_string, expected):
    assert parse_insertion_rules(input_string) == expected


def parse_insertion_rules(input_string):
    result = {}
    for line in input_string.strip().split("\n")[2:]:
        [key, value] = line.split(" -> ")
        result[key] = value
    return result


def part_a(filepath: str):
    with open(filepath, "r") as file:
        pass


def part_b(filepath: str):
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    day = 14
    input_file = f"../puzzle_input/day{day}.txt"
    print(f"The answer to {day}A is: {part_a(input_file)}")
    print(f"The answer to {day}B is: {part_b(input_file)}")
