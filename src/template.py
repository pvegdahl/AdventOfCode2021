import pytest


@pytest.mark.parametrize("input_string, expected", [])
def test_parse_input(input_string, expected):
    assert parse_input(input_string) == expected


def parse_input(input_string):
    pass


def part_a(filepath: str):
    with open(filepath, "r") as file:
        pass


def part_b(filepath: str):
    with open(filepath, "r") as file:
        pass


DAY = 0

if __name__ == "__main__":
    print(f"The answer to {DAY}A is: {part_a('../puzzle_input/day{DAY}.txt')}")
    print(f"The answer to {DAY}B is: {part_b('../puzzle_input/day{DAY}.txt')}")
