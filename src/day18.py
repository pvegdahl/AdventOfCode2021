import math
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
            (1, (2, (3, (4, (5, 6))))),
            None,
            ExplosionSpec(index=(1, 1, 1, 1), left_value=5, right_value=6),
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


def find_left_neighbor_index(
    snail_fish_number, index: Tuple[int, ...]
) -> Optional[Tuple[int, ...]]:
    if not any(index):
        return None
    else:
        last_one_at = find_index_of_last_value(index, 1)
        left_index = index[0:last_one_at] + (0,)
        while is_tuple_at_location(snail_fish_number, left_index):
            left_index += (1,)
        return left_index


def is_tuple_at_location(snail_fish_number, index: Tuple[int, ...]):
    value_at_index = get_value_at_index(
        snail_fish_number=snail_fish_number, index=index
    )
    return isinstance(value_at_index, tuple)


def get_value_at_index(snail_fish_number, index):
    value_at_index = snail_fish_number
    for i in index:
        value_at_index = value_at_index[i]
    return value_at_index


def find_index_of_last_value(tt: Tuple[int, ...], target_value):
    for i in reversed(range(len(tt))):
        if tt[i] == target_value:
            return i
    return None


@pytest.mark.parametrize(
    "snail_fish_number, index, expected",
    [
        ((((((1, 2), 3), 4), 5), 6), (0, 0, 0, 0), None),
        ((1, (2, (3, (4, (5, 6))))), (1, 1, 1, 1), (1, 1, 1, 0)),
        ((1, (2, (3, ((4, 5), 6)))), (1, 1, 1, 0), (1, 1, 0)),
        ((1, (2, ((3, 4), ((4, 5), 6)))), (1, 1, 1, 0), (1, 1, 0, 1)),
        (((1, (2, (3, 4))), ((((10, 9), 8), 7), 6)), (1, 0, 0, 0), (0, 1, 1, 1)),
    ],
)
def test_find_left_neighbor_index(snail_fish_number, index, expected):
    assert (
        find_left_neighbor_index(snail_fish_number=snail_fish_number, index=index)
        == expected
    )


def find_right_neighbor_index(snail_fish_number, index: Tuple[int, ...]):
    if all(index):
        return None
    else:
        last_zero_at = find_index_of_last_value(index, 0)
        left_index = index[:last_zero_at] + (1,)
        while is_tuple_at_location(snail_fish_number, left_index):
            left_index += (0,)
        return left_index


@pytest.mark.parametrize(
    "snail_fish_number, index, expected",
    [
        ((((((1, 2), 3), 4), 5), 6), (0, 0, 0, 0), (0, 0, 0, 1)),
        ((1, (2, (3, (4, (5, 6))))), (1, 1, 1, 1), None),
        ((1, (2, (3, ((4, 5), 6)))), (1, 1, 1, 0), (1, 1, 1, 1)),
        ((1, (2, ((3, 4), ((4, 5), 6)))), (1, 1, 1, 0), (1, 1, 1, 1)),
        (((1, (2, (3, 4))), ((((10, 9), 8), 7), 6)), (1, 0, 0, 0), (1, 0, 0, 1)),
    ],
)
def test_find_right_neighbor_index(snail_fish_number, index, expected):
    assert (
        find_right_neighbor_index(snail_fish_number=snail_fish_number, index=index)
        == expected
    )


class ExplodeReplaceCommand:
    def __init__(self, spec: ExplosionSpec, snail_fish_number):
        self.snail_fish_number = snail_fish_number
        self.explosion_spec = spec
        self.left_index = find_left_neighbor_index(
            snail_fish_number=snail_fish_number, index=spec.index
        )
        self.right_index = find_right_neighbor_index(
            snail_fish_number=snail_fish_number, index=spec.index
        )

    def get_value(self, index: Tuple[int, ...]) -> Union[Tuple, int]:
        if index == self.explosion_spec.index:
            return 0

        value_at_index = get_value_at_index(
            snail_fish_number=self.snail_fish_number, index=index
        )
        if index == self.left_index:
            return value_at_index + self.explosion_spec.left_value
        if index == self.right_index:
            return value_at_index + self.explosion_spec.right_value
        if isinstance(value_at_index, int):
            return value_at_index
        return tuple(self.get_value(index + (i,)) for i in range(len(value_at_index)))


def explode(snail_fish_number, index_so_far: Tuple[int, ...] = None):
    explosion_spec = find_first_explosion(snail_fish_number)
    if not explosion_spec:
        return snail_fish_number
    return ExplodeReplaceCommand(
        spec=explosion_spec, snail_fish_number=snail_fish_number
    ).get_value(tuple())


@pytest.mark.parametrize(
    "snail_fish_number, expected",
    [
        (((((0, 1), 2), 3), 4), ((((0, 1), 2), 3), 4)),
        ((((((9, 8), 1), 2), 3), 4), ((((0, 9), 2), 3), 4)),
        ((7, (6, (5, (4, (3, 2))))), (7, (6, (5, (7, 0))))),
        (((6, (5, (4, (3, 2)))), 1), ((6, (5, (7, 0))), 3)),
        (
            ((3, (2, (1, (7, 3)))), (6, (5, (4, (3, 2))))),
            ((3, (2, (8, 0))), (9, (5, (4, (3, 2))))),
        ),
        (
            ((3, (2, (8, 0))), (9, (5, (4, (3, 2))))),
            ((3, (2, (8, 0))), (9, (5, (7, 0)))),
        ),
    ],
)
def test_explode(snail_fish_number, expected):
    assert explode(snail_fish_number) == expected


def split_sfn(snail_fish_number):
    if isinstance(snail_fish_number, int):
        if snail_fish_number >= 10:
            return split_number(snail_fish_number)
        else:
            return snail_fish_number
    return tuple(split_sfn(sub_number) for sub_number in snail_fish_number)


def split_number(number):
    a = math.floor(number / 2.0)
    b = number - a
    return a, b


@pytest.mark.parametrize("snail_fish_number, expected", [
    ((1, 2), (1, 2)),
    ((10, 2), ((5, 5), 2)),
    ((11, 2), ((5, 6), 2)),
    ((1, 12), (1, (6, 6))),
    ((1, 13), (1, (6, 7))),
    ((1, (2, 10)), (1, (2, (5, 5)))),
    ((1, (2, (3, 10))), (1, (2, (3, (5, 5))))),
    ((11, 12), ((5, 6), 12)),
])
def test_split_sfn(snail_fish_number, expected):
    assert split_sfn(snail_fish_number) == expected


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
