from typing import List

import pytest


@pytest.mark.parametrize("input_list, expected_count", [
    ([], 0),
    ([1], 0),
    ([1, 0], 0),
    ([1, 2], 1),
    ([1, 2, 1], 1),
    ([1, 2, 3], 2),
    ([1, 2, 3, 2, 4, 10, 4, 2, 6], 5),
])
def test_count_increase(input_list, expected_count):
    assert count_increase(input_list) == expected_count


def count_increase(numbers: List[int]) -> int:
    count = 0
    if len(numbers) < 2:
        return count

    for i in range(len(numbers)-1):
        if numbers[i] < numbers[i+1]:
            count += 1
    return count
