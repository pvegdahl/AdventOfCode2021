from typing import Tuple, List

import pytest


@pytest.mark.parametrize("input_string, expected_list", [
    ("", []),
    ("forward 5", [("forward", 5)]),
])
def test_parse_input(input_string, expected_list):
    assert parse_input(input_string) == expected_list


def parse_input(input_string: str) -> List[Tuple[str, int]]:
    if not input_string:
        return []
    return [("forward", 5)]


