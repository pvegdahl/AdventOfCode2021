import pytest


@pytest.mark.parametrize("input_string, expected", [])
def test_parse_input(input_string, expected):
    assert parse_input(input_string) == expected


def parse_input(input_string):
    pass


def explode(snail_fish_number, depth: int = 0):
    if isinstance(snail_fish_number, int):
        return snail_fish_number
    return tuple(
        explode(snail_fish_number=sub_sfn, depth=depth + 1)
        for sub_sfn in snail_fish_number
    )


@pytest.mark.parametrize(
    "snail_fish_number, expected",
    [
        (((((0, 1), 2), 3), 4), ((((0, 1), 2), 3), 4)),
        # ((((((9, 8), 1), 2), 3), 4), ((((0, 9), 2), 3), 4)),
    ],
)
def test_explode(snail_fish_number, expected):
    assert explode(snail_fish_number) == expected


def part_a(filepath: str):
    with open(filepath, "r") as file:
        pass


def part_b(filepath: str):
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    day = 18
    input_file = f"../puzzle_input/day{day}.txt"
    print(f"The answer to {day}A is: {part_a(input_file)}")
    print(f"The answer to {day}B is: {part_b(input_file)}")
