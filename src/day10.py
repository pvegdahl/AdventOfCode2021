from typing import Optional, List, Any

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

START_TO_END = {value: key for key, value in END_TO_START.items()}


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


class Stack:
    def __init__(self, initial_stack: Optional[List] = None):
        if initial_stack:
            self.stack = initial_stack
        else:
            self.stack = []

    def size(self):
        return len(self.stack)

    def push(self, value):
        self.stack.append(value)

    def pop(self) -> Any:
        return self.stack.pop()

    def handle_value(self, value):
        if value in START_TO_END:
            self.push(value)
        elif value in END_TO_START:
            if not self.stack or self.stack[-1] != END_TO_START[value]:
                raise Exception(value)
            self.pop()


@pytest.mark.parametrize("stack, expected", [
    (Stack(), 0),
    (Stack([]), 0),
    (Stack([1, 2, 3]), 3),
    (Stack(["a", "b", "c", "d"]), 4),
])
def test_stack_size(stack, expected):
    assert stack.size() == expected


@pytest.mark.parametrize("items, expected", [
    ([], 0),
    ([1], 1),
    ([1, 2, 3], 3),
])
def test_stack_push_pop(items, expected):
    stack = Stack()
    size = 0
    for item in items:
        stack.push(item)
        size += 1
        assert stack.size() == size
    assert stack.size() == expected
    for item in reversed(items):
        assert stack.pop() == item
        size -= 1
        assert stack.size() == size


@pytest.mark.parametrize("stack, new_value, expected", [
    (Stack(), "{", Stack(["{"])),
    (Stack(["("]), "{", Stack(["(", "{"])),
    (Stack(["("]), ")", Stack()),
    (Stack(["(", "{"]), "}", Stack(["("])),
])
def test_stack_handle_value(stack, new_value, expected):
    stack.handle_value(new_value)
    assert stack.stack == expected.stack


@pytest.mark.parametrize("stack, new_value", [
    (Stack(), "}"),
    (Stack(["("]), "}"),
    (Stack(["{", "("]), "}"),
])
def test_stack_handle_value_throws_exception(stack, new_value):
    with pytest.raises(Exception):
        stack.handle_value(new_value)


@pytest.mark.parametrize("input_string, expected", [
    ("", ""),
    ("(", ")"),
    ("<", ">"),
    ("<><", ">"),
    ("<<", ">>"),
    ("<<>", ">"),
    ("[({(<(())[]>[[{[]{<()<>>", "}}]])})]"),
    ("[(()[<>])]({[<{<<[]>>(", ")}>]})"),
    ("(((({<>}<{<{<>}{[]{[]{}", "}}>}>))))"),
    ("{<[[]]>}<{[{[{[]{()[[[]", "]]}}]}]}>"),
    ("<{([{{}}[<[[[<>{}]]]>[]]", "])}>"),
])
def test_get_completion_string(input_string, expected):
    assert get_completion_string(input_string) == expected


def get_completion_string(input_string):
    stack = Stack()
    # noinspection PyBroadException
    try:
        for char in input_string:
            stack.handle_value(char)
    except Exception:
        return None
    result = []
    while stack.size():
        result.append(START_TO_END[stack.pop()])
    return "".join(result)


SCORE_MAP_2 = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


@pytest.mark.parametrize("completion_string, expected", [
    ("", 0),
    (")", 1),
    ("]", 2),
    ("}", 3),
    (">", 4),
    (")]", 7),
    ("}}]])})]", 288957),
    (")}>]})", 5566),
    ("}}>}>))))", 1480781),
    ("]]}}]}]}>", 995444),
    ("])}>", 294),
])
def test_calculate_completion_score(completion_string, expected):
    assert calculate_completion_score(completion_string) == expected


def calculate_completion_score(completion_string):
    result = 0
    for char in completion_string:
        result *= 5
        result += SCORE_MAP_2[char]
    return result


@pytest.mark.parametrize("input_string, expected", [
    ("", 0),
    ("(", 1),
    ("}", 0),
    ("""
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
    """, 288957),
("""
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
    """, 288957),
])
def test_score_lines_2(input_string, expected):
    assert score_lines_2(input_string) == expected


def score_lines_2(input_string: str) -> int:
    scores = []
    for line in input_string.strip().split("\n"):
        completion_string = get_completion_string(line)
        if completion_string:
            scores.append(calculate_completion_score(completion_string))
    if not scores:
        return 0
    middle_index = int((len(scores) - 1) / 2)
    return sorted(scores)[middle_index]


def day10a(filepath: str) -> int:
    with open(filepath, "r") as file:
        return score_lines(file.read())


def day10b(filepath: str) -> int:
    with open(filepath, "r") as file:
        return score_lines_2(file.read())


if __name__ == "__main__":
    print(f"The answer to 10A is: {day10a('../puzzle_input/day10.txt')}")
    print(f"The answer to 10B is: {day10b('../puzzle_input/day10.txt')}")
