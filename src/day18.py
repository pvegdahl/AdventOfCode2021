from typing import Union, Tuple, NamedTuple, Optional

import pytest


@pytest.mark.parametrize("input_string, expected", [])
def test_parse_input(input_string, expected):
    assert parse_input(input_string) == expected


def parse_input(input_string):
    pass


class ExplosionSpec(NamedTuple):
    index: Tuple[int, ...]
    left_value: int
    right_value: int


def explode(snail_fish_number):
    explosion_spec = find_first_explosion(snail_fish_number)
    if not explosion_spec:
        return snail_fish_number


@pytest.mark.parametrize(
    "snail_fish_number, index_so_far, expected",
    [
        ((1, 2), None, None),
        ((1, 2), (0,), None),
        ((1, 2), (0, 0), None),
        ((1, 2), (0, 0, 0), None),
        (
            (1, 2),
            (0, 0, 0, 0),
            ExplosionSpec(index=(0, 0, 0, 0), left_value=1, right_value=2),
        ),
        (((1, 2), 3), None, None),
        (((1, 2), 3), (0, 0), None),
        (
            ((1, 2), 3),
            (0, 0, 0),
            ExplosionSpec(index=(0, 0, 0, 0), left_value=1, right_value=2),
        ),
        (
            (((1, 2), 3), 4),
            (0, 0),
            ExplosionSpec(index=(0, 0, 0, 0), left_value=1, right_value=2),
        ),
        (
            ((((1, 2), 3), 4), 5),
            (0,),
            ExplosionSpec(index=(0, 0, 0, 0), left_value=1, right_value=2),
        ),
        (
            (((((1, 2), 3), 4), 5), 6),
            None,
            ExplosionSpec(index=(0, 0, 0, 0), left_value=1, right_value=2),
        ),
        (
            (((((9, 8), 1), 2), 3), 4),
            None,
            ExplosionSpec(index=(0, 0, 0, 0), left_value=9, right_value=8),
        ),
        (
            (1, (2, (3, ((4, 5), 6)))),
            None,
            ExplosionSpec(index=(1, 1, 1, 0), left_value=4, right_value=5),
        ),
        (
            (((((1, 2), 3), 4), 5), (6, (7, (8, (9, 10))))),
            None,
            ExplosionSpec(index=(0, 0, 0, 0), left_value=1, right_value=2),
        ),
    ],
)
def test_find_first_explosion(snail_fish_number, index_so_far, expected):
    assert (
        find_first_explosion(snail_fish_number, index_so_far=index_so_far) == expected
    )


def find_first_explosion(
    snail_fish_number, index_so_far: Tuple[int, ...] = None
) -> Optional[ExplosionSpec]:
    if index_so_far is None:
        index_so_far = tuple()

    if isinstance(snail_fish_number, int):
        return None

    if len(index_so_far) == 4:
        return ExplosionSpec(
            index=index_so_far,
            left_value=snail_fish_number[0],
            right_value=snail_fish_number[1],
        )
    else:
        for i in range(len(snail_fish_number)):
            new_index_so_far = index_so_far + (i,)
            result = find_first_explosion(
                snail_fish_number=snail_fish_number[i], index_so_far=new_index_so_far
            )
            if result:
                return result
    return None


def test_find_left_neighbor(
    snail_fish_number, index: Tuple[int, ...]
) -> Tuple[int, ...]:
    pass


def explode_recursive(
    snail_fish_number, depth: int = 0
) -> Tuple[Union[Tuple, int], int]:
    if isinstance(snail_fish_number, int):
        return snail_fish_number, 0
    elif depth == 4:
        return 0, snail_fish_number[1]
    else:
        result = []
        for sub_sfn in snail_fish_number:
            new_sub_sfn, explode_right = explode_recursive(
                snail_fish_number=sub_sfn, depth=depth + 1
            )
            result.append(new_sub_sfn)
        return (
            tuple(
                explode_recursive(snail_fish_number=sub_sfn, depth=depth + 1)
                for sub_sfn in snail_fish_number
            ),
            0,
        )


@pytest.mark.parametrize(
    "snail_fish_number, expected",
    [
        (((((0, 1), 2), 3), 4), ((((0, 1), 2), 3), 4)),
        ((((((9, 8), 1), 2), 3), 4), ((((0, 9), 2), 3), 4)),
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
