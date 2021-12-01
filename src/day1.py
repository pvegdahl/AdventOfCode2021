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


@pytest.mark.parametrize("input_string, expected_list", [
    ("", []),
    ("123", [123]),
    ("1\n2", [1, 2]),
    ("\n\n", []),
    ("1\n2\n", [1, 2]),
    ("1  \n   2\n3\n4", [1, 2, 3, 4]),
])
def test_get_numbers_from_string(input_string, expected_list):
    assert get_numbers_from_string(input_string) == expected_list


def get_numbers_from_string(input_string: str) -> List[int]:
    if not input_string.split():
        return []

    result = []
    input_parsed = input_string.strip().split("\n")
    for value in input_parsed:
        result.append(int(value))
    return result


@pytest.mark.parametrize("input_list, expected_list", [
    ([], []),
    ([1], []),
    ([1, 2], []),
    ([1, 2, 3], [6]),
    ([1, 2, 3, 4], [6, 9]),
])
def test_calculate_sliding_window_sums(input_list, expected_list):
    assert calculate_sliding_window_sums(input_list) == expected_list


def calculate_sliding_window_sums(input_list: List[int]) -> List[int]:
    if len(input_list) == 3:
        return [sum(input_list)]
    elif len(input_list) == 4:
        return [sum(input_list[:3]), sum(input_list[1:])]
    return []


def day_1a(filepath: str) -> int:
    with open(filepath, "r") as file:
        numbers = get_numbers_from_string(file.read())
    return count_increase(numbers)


if __name__ == "__main__":
    print(f"The answer to 1A is: {day_1a('../puzzle_input/day1.txt')}")
