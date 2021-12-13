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


if __name__ == "__main__":
    day = 0
    input_file = f"../puzzle_input/day{day}.txt"
    print(f"The answer to {day}A is: {part_a(input_file)}")
    print(f"The answer to {day}B is: {part_b(input_file)}")
