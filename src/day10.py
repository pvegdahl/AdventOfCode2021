from typing import Optional

import pytest


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("}", "}"),
        (">", ">"),
        ("{>", ">"),
        ("{}>", ">"),
        ("{>}", ">"),
        ("{}", None),
        ("[", None),
        ("[](<{})>", ")"),
    ],
)
def test_find_first_corrupted_char(input_string, expected):
    assert find_first_corrupted_char(input_string) == expected


END_TO_START = {
    "}": "{",
    "]": "[",
    ">": "<",
    ")": "(",
}


def find_first_corrupted_char(input_string: str) -> Optional[str]:
    stack = []
    for char in input_string:
        if char in END_TO_START.keys():
            if not stack:
                return char
            elif END_TO_START[char] == stack[-1]:
                stack.pop()
            else:
                return char
        else:
            stack.append(char)
    return None


CHAR_TO_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("", 0),
        (")", 3),
        ("]", 57),
        ("}", 1197),
        (">", 25137),
        (")\n]", 60),
        ("]\n)", 60),
        ("())\n]", 60),
        ("())\n]\n()\n", 60),
        ("""[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""", 26397)
    ])
def test_score_lines(input_string, expected):
    assert score_lines(input_string) == expected


def score_lines(input_string: str) -> int:
    result = 0
    for line in input_string.strip().split("\n"):
        result += CHAR_TO_SCORE.get(find_first_corrupted_char(line)) or 0
    return result


def day10a(filepath: str) -> int:
    with open(filepath, "r") as file:
        return score_lines(file.read())


def day10b(filepath: str) -> int:
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    print(f"The answer to 10A is: {day10a('../puzzle_input/day10.txt')}")
    print(f"The answer to 10B is: {day10b('../puzzle_input/day10.txt')}")
