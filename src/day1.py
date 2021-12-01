from typing import List

import pytest


@pytest.mark.parametrize("input_list, expected_count", [
    ([], 0),
    ([1], 0),
    ([1, 0], 0),
    ([1, 2], 1),
])
def test_count_increase(input_list, expected_count):
    assert count_increase(input_list) == expected_count


def count_increase(numbers: List[int]) -> int:
    if len(numbers) < 2:
        return 0
    return 1 if numbers[0] < numbers[1] else 0
