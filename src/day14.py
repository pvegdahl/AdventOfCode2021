from collections import defaultdict
from typing import Dict

import pytest


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("", ""),
        ("ABC", "ABC"),
        ("ABC\n", "ABC"),
        ("ABC\n\n", "ABC"),
        ("ABC\n\nAB -> C", "ABC"),
    ],
)
def test_parse_polymer_template(input_string, expected):
    assert parse_polymer_template(input_string) == expected


def parse_polymer_template(input_string: str) -> str:
    if not input_string:
        return ""
    return input_string.split("\n")[0].strip()


@pytest.mark.parametrize(
    "polymer, expected",
    [
        ("", {}),
        ("AB", {"AB": 1, "B": 1}),
        ("ABC", {"AB": 1, "BC": 1, "C": 1}),
        ("ABCABCAB", {"AB": 3, "BC": 2, "CA": 2, "B": 1}),
    ],
)
def test_parse_polymer_pair_dict(polymer, expected):
    assert parse_polymer_pair_dict(polymer) == expected


# This name is a little off.  It will record the count of all pairs, but also contain the final single element.  This
# works for our purposes because that element will never morph, and it will make our counting at the end work.
def parse_polymer_pair_dict(polymer: str) -> Dict[str, int]:
    result = defaultdict(lambda: 0)
    for i in range(len(polymer)):
        result[polymer[i:i+2]] += 1
    return result


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("", {}),
        ("ABC\n\n", {}),
        ("ABC\n\nAB -> C", {"AB": "C"}),
        ("ABC\n\nAB -> C\nCA -> B", {"AB": "C", "CA": "B"}),
    ],
)
def test_parse_insertion_rules(input_string, expected):
    assert parse_insertion_rules(input_string) == expected


def parse_insertion_rules(input_string: str) -> Dict[str, str]:
    result = defaultdict(lambda: "")
    for line in input_string.strip().split("\n")[2:]:
        [key, value] = line.split(" -> ")
        result[key] = value
    return result


@pytest.mark.parametrize(
    "polymer, insertion_rules, expected",
    [
        ("AB", defaultdict(lambda: "", {"CD": "E"}), "AB"),
        ("AB", defaultdict(lambda: "", {"AB": "C"}), "ACB"),
        ("AB", defaultdict(lambda: "", {"AB": "C", "CB": "D"}), "ACB"),
        ("ABC", defaultdict(lambda: "", {"AB": "C", "BC": "D"}), "ACBDC"),
    ],
)
def test_polymer_insertion(polymer, insertion_rules, expected):
    assert (
        polymer_insertion(polymer=polymer, insertion_rules=insertion_rules) == expected
    )


@pytest.fixture
def aoc_example_input():
    return """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


@pytest.fixture
def aoc_polymer(aoc_example_input):
    return parse_polymer_template(aoc_example_input)


@pytest.fixture
def aoc_insertion_rules(aoc_example_input):
    return parse_insertion_rules(aoc_example_input)


def test_polymer_insertion_aoc_example(aoc_polymer, aoc_insertion_rules):
    step_1_polymer = polymer_insertion(
        polymer=aoc_polymer, insertion_rules=aoc_insertion_rules
    )
    assert step_1_polymer == "NCNBCHB"
    step_2_polymer = polymer_insertion(
        polymer=step_1_polymer, insertion_rules=aoc_insertion_rules
    )
    assert step_2_polymer == "NBCCNBBBCBHCB"
    step_3_polymer = polymer_insertion(
        polymer=step_2_polymer, insertion_rules=aoc_insertion_rules
    )
    assert step_3_polymer == "NBBBCNCCNBBNBNBBCHBHHBCHB"
    step_4_polymer = polymer_insertion(
        polymer=step_3_polymer, insertion_rules=aoc_insertion_rules
    )
    assert step_4_polymer == "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"


def polymer_insertion(polymer: str, insertion_rules: Dict[str, str]):
    result = ""
    for i in range(len(polymer)):
        result += polymer[i]
        result += insertion_rules[polymer[i : i + 2]]
    return result


@pytest.mark.parametrize("polymer_dict, insertion_rules, expected", [
    ({}, {"AB": "C"}, {}),
    ({"AB": 1, "B": 1}, {"AB": "C"}, {"AC": 1, "CB": 1, "B": 1}),
    ({"AB": 1, "B": 1, "DE": 55}, {"AB": "C"}, {"AC": 1, "CB": 1, "B": 1, "DE": 55}),
])
def test_polymer_insertion_on_dict(polymer_dict, insertion_rules, expected):
    assert polymer_insertion_on_dict(polymer_dict=polymer_dict, insertion_rules=insertion_rules) == expected


def polymer_insertion_on_dict(polymer_dict: Dict[str, int], insertion_rules: Dict[str, str]) -> Dict[str, int]:
    result = defaultdict(lambda: 0)
    for polymer_pair, count in polymer_dict.items():
        if polymer_pair in insertion_rules:
            new_char = insertion_rules[polymer_pair]
            pair_a = f"{polymer_pair[0]}{new_char}"
            pair_b = f"{new_char}{polymer_pair[1]}"
            result[pair_a] += count
            result[pair_b] += count
        else:
            result[polymer_pair] += count
    return result


@pytest.mark.parametrize(
    "steps, expected",
    [
        (1, "NCNBCHB"),
        (2, "NBCCNBBBCBHCB"),
        (3, "NBBBCNCCNBBNBNBBCHBHHBCHB"),
        (4, "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"),
    ],
)
def test_run_n_steps(steps, expected, aoc_polymer, aoc_insertion_rules):
    assert (
        run_n_steps(
            polymer=aoc_polymer, insertion_rules=aoc_insertion_rules, steps=steps
        )
        == expected
    )


@pytest.mark.parametrize(
    "steps, expected",
    [
        (5, 97),
        (10, 3073),
    ],
)
def test_run_n_steps_length(steps, expected, aoc_polymer, aoc_insertion_rules):
    assert (
        len(
            run_n_steps(
                polymer=aoc_polymer, insertion_rules=aoc_insertion_rules, steps=steps
            )
        )
        == expected
    )


def run_n_steps(polymer, insertion_rules, steps):
    result = polymer
    for _ in range(steps):
        result = polymer_insertion(polymer=result, insertion_rules=insertion_rules)
    return result


@pytest.mark.parametrize(
    "text, expected",
    [
        ("", {}),
        ("A", {"A": 1}),
        ("AAAA", {"A": 4}),
        ("AB", {"A": 1, "B": 1}),
        ("ABACCDBBB", {"A": 2, "B": 4, "C": 2, "D": 1}),
    ],
)
def test_count_letters(text, expected):
    assert count_letters(text) == expected


def count_letters(text: str) -> Dict[str, int]:
    return count_letters_dict(parse_polymer_pair_dict(text))


def count_letters_dict(polymer_dict: Dict[str, int]) -> Dict[str, int]:
    result = defaultdict(lambda: 0)
    for pair, count in polymer_dict.items():
        result[pair[0]] += count
    return result


@pytest.mark.parametrize(
    "text, expected",
    [
        ("A", 1),
        ("AAB", 1),
        ("AAABB", 2),
        ("AAABBBBBBBCCCCAA", 4),
    ],
)
def test_get_least_common_letter_count(text, expected):
    assert get_least_common_letter_count(text) == expected


def get_least_common_letter_count(text: str) -> int:
    return min(count_letters(text).values())


@pytest.mark.parametrize(
    "text, expected",
    [
        ("A", 1),
        ("AAB", 2),
        ("AAABB", 3),
        ("AAABBBBBBBCCCCAA", 7),
    ],
)
def test_get_most_common_letter_count(text, expected):
    assert get_most_common_letter_count(text) == expected


def get_most_common_letter_count(text: str) -> int:
    return max(count_letters(text).values())


def test_find_max_min_difference(aoc_example_input):
    assert find_max_min_difference(input_text=aoc_example_input, steps=10) == 1588


def find_max_min_difference(input_text: str, steps: int) -> int:
    polymer = parse_polymer_template(input_text)
    insertion_rules = parse_insertion_rules(input_text)
    final_polymer = run_n_steps(polymer=polymer, insertion_rules=insertion_rules, steps=steps)
    return get_most_common_letter_count(final_polymer) - get_least_common_letter_count(final_polymer)


def part_a(filepath: str):
    with open(filepath, "r") as file:
        return find_max_min_difference(input_text=file.read(), steps=10)


def part_b(filepath: str):
    with open(filepath, "r") as file:
        return find_max_min_difference(input_text=file.read(), steps=40)


if __name__ == "__main__":
    day = 14
    input_file = f"../puzzle_input/day{day}.txt"
    print(f"The answer to {day}A is: {part_a(input_file)}")
    print(f"The answer to {day}B is: {part_b(input_file)}")
