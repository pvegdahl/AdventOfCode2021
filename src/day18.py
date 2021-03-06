import json
import math
from typing import Union, Tuple, NamedTuple, Optional, List

import pytest


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("1", [1]),
        ("[1,2]", [(1, 2)]),
        ("[[[7,1],2],3]\n[[1,7],7]", [(((7, 1), 2), 3), ((1, 7), 7)]),
    ],
)
def test_parse_input(input_string, expected):
    assert parse_input(input_string) == expected


def parse_input(input_string: str):
    return [parse_line(line) for line in input_string.strip().split("\n")]


def parse_line(line: str):
    return nested_lists_to_nested_tuples(json.loads(line))


def nested_lists_to_nested_tuples(as_list):
    if not isinstance(as_list, List):
        return as_list
    return tuple(nested_lists_to_nested_tuples(i) for i in as_list)


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


class SplitSfnCommand:
    def __init__(self):
        self.split_count = 0

    def split(self, snail_fish_number):
        if self.split_count > 0:
            return snail_fish_number

        if isinstance(snail_fish_number, int):
            if snail_fish_number >= 10:
                return self.split_number(snail_fish_number)
            else:
                return snail_fish_number
        return tuple(self.split(sub_number) for sub_number in snail_fish_number)

    def split_number(self, number):
        self.split_count += 1
        a = math.floor(number / 2.0)
        b = number - a
        return a, b


@pytest.mark.parametrize(
    "snail_fish_number, expected",
    [
        ((1, 2), (1, 2)),
        ((10, 2), ((5, 5), 2)),
        ((11, 2), ((5, 6), 2)),
        ((1, 12), (1, (6, 6))),
        ((1, 13), (1, (6, 7))),
        ((1, (2, 10)), (1, (2, (5, 5)))),
        ((1, (2, (3, 10))), (1, (2, (3, (5, 5))))),
        ((11, 12), ((5, 6), 12)),
    ],
)
def test_split_sfn(snail_fish_number, expected):
    assert SplitSfnCommand().split(snail_fish_number) == expected


def sfn_add(sfn_a, sfn_b):
    return sfn_a, sfn_b


@pytest.mark.parametrize(
    "sfn_a, sfn_b, expected",
    [
        ((1, 2), (3, 4), ((1, 2), (3, 4))),
        ((1, (2, (3, 4))), ((5, 6), 7), ((1, (2, (3, 4))), ((5, 6), 7))),
    ],
)
def test_sfn_add(sfn_a, sfn_b, expected):
    assert sfn_add(sfn_a, sfn_b) == expected


def sfn_reduce(sfn):
    previous_sfn = None
    while sfn != previous_sfn:
        while sfn != previous_sfn:
            previous_sfn = sfn
            sfn = explode(previous_sfn)
        sfn = SplitSfnCommand().split(sfn)
    return sfn


@pytest.mark.parametrize(
    "sfn, expected",
    [
        ((1, 2), (1, 2)),
        ((((((9, 8), 1), 2), 3), 4), ((((0, 9), 2), 3), 4)),
        (
            ((3, (2, (1, (7, 3)))), (6, (5, (4, (3, 2))))),
            ((3, (2, (8, 0))), (9, (5, (7, 0)))),
        ),
        ((1, 13), (1, (6, 7))),
        ((12, 13), ((6, 6), (6, 7))),
        (
            (((((4, 3), 4), 4), (7, ((8, 4), 9))), (1, 1)),
            ((((0, 7), 4), ((7, 8), (6, 0))), (8, 1)),
        ),
    ],
)
def test_sfn_reduce(sfn, expected):
    assert sfn_reduce(sfn) == expected


def add_and_reduce_many_sfns(sfns: List[Tuple]):
    result = sfns[0]
    for sfn in sfns[1:]:
        result = sfn_reduce(sfn_add(result, sfn))
    return result


def test_add_and_reduce_many_sfns():
    assert add_and_reduce_many_sfns(
        [
            (((0, (4, 5)), (0, 0)), (((4, 5), (2, 6)), (9, 5))),
            (7, (((3, 7), (4, 3)), ((6, 3), (8, 8)))),
            ((2, ((0, 8), (3, 4))), (((6, 7), 1), (7, (1, 6)))),
            ((((2, 4), 7), (6, (0, 5))), (((6, 8), (2, 8)), ((2, 1), (4, 5)))),
            (7, (5, ((3, 8), (1, 4)))),
            ((2, (2, 2)), (8, (8, 1))),
            (2, 9),
            (1, (((9, 3), 9), ((9, 0), (0, 7)))),
            (((5, (7, 4)), 7), 1),
            ((((4, 2), 2), 6), (8, 7)),
        ]
    ) == (
        (((8, 7), (7, 7)), ((8, 6), (7, 7))),
        (((0, 7), (6, 6)), (8, 7)),
    )


def sfn_magnitude(sfn):
    if isinstance(sfn, int):
        return sfn
    return 3 * sfn_magnitude(sfn[0]) + 2 * sfn_magnitude(sfn[1])


@pytest.mark.parametrize(
    "sfn, expected",
    [
        ((1, 2), 7),
        ((9, 1), 29),
        (((1, 2), ((3, 4), 5)), 143),
        (((((8, 7), (7, 7)), ((8, 6), (7, 7))), (((0, 7), (6, 6)), (8, 7))), 3488),
    ],
)
def test_sfn_magnitude(sfn, expected):
    assert sfn_magnitude(sfn) == expected


def do_homework(sfns):
    return sfn_magnitude(add_and_reduce_many_sfns(sfns))


EXAMPLE_HOMEWORK = [
    (((0, (5, 8)), ((1, 7), (9, 6))), ((4, (1, 2)), ((1, 4), 2))),
    (((5, (2, 8)), 4), (5, ((9, 9), 0))),
    (6, (((6, 2), (5, 6)), ((7, 6), (4, 7)))),
    (((6, (0, 7)), (0, 9)), (4, (9, (9, 0)))),
    (((7, (6, 4)), (3, (1, 3))), (((5, 5), 1), 9)),
    ((6, ((7, 3), (3, 2))), (((3, 8), (5, 7)), 4)),
    ((((5, 4), (7, 7)), 8), ((8, 3), 8)),
    ((9, 3), ((9, 9), (6, (4, 9)))),
    ((2, ((7, 7), 7)), ((5, 8), ((9, 3), (0, 2)))),
    ((((5, 2), 5), (8, (3, 7))), ((5, (7, 5)), (4, 4))),
]


def test_do_homework():
    assert do_homework(EXAMPLE_HOMEWORK) == 4140


def do_homework_part_2(sfns):
    max_value = 0
    for pair in get_all_pairs(sfns):
        max_value = max(max_value, do_homework(pair))
    return max_value


def get_all_pairs(sfns):
    for i in range(len(sfns)):
        for j in range(len(sfns)):
            if i != j:
                yield [sfns[i], sfns[j]]


def test_do_homework_part_2():
    assert do_homework_part_2(EXAMPLE_HOMEWORK) == 3993


def part_a(filepath: str):
    with open(filepath, "r") as file:
        sfns = parse_input(file.read())
    return do_homework(sfns)


def part_b(filepath: str):
    with open(filepath, "r") as file:
        sfns = parse_input(file.read())
    return do_homework_part_2(sfns)


if __name__ == "__main__":
    day = 18
    input_file = f"../puzzle_input/day{day}.txt"
    print(f"The answer to {day}A is: {part_a(input_file)}")
    print(f"The answer to {day}B is: {part_b(input_file)}")
