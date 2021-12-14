from collections import defaultdict
from typing import Dict

import pytest


@pytest.mark.parametrize("input_string, expected", [
    ("", ""),
    ("ABC", "ABC"),
    ("ABC\n", "ABC"),
    ("ABC\n\n", "ABC"),
    ("ABC\n\nAB -> C", "ABC"),
])
def test_parse_polymer_template(input_string, expected):
    assert parse_polymer_template(input_string) == expected


def parse_polymer_template(input_string: str) -> str:
    if not input_string:
        return ""
    return input_string.split("\n")[0].strip()


@pytest.mark.parametrize("input_string, expected", [
    ("", {}),
    ("ABC\n\n", {}),
    ("ABC\n\nAB -> C", {"AB": "C"}),
    ("ABC\n\nAB -> C\nCA -> B", {"AB": "C", "CA": "B"}),
])
def test_parse_insertion_rules(input_string, expected):
    assert parse_insertion_rules(input_string) == expected


def parse_insertion_rules(input_string: str) -> Dict[str, str]:
    result = defaultdict(lambda: "")
    for line in input_string.strip().split("\n")[2:]:
        [key, value] = line.split(" -> ")
        result[key] = value
    return result


@pytest.mark.parametrize("polymer, insertion_rules, expected", [
    ("AB", defaultdict(lambda: "", {"CD": "E"}), "AB"),
    ("AB", defaultdict(lambda: "", {"AB": "C"}), "ACB"),
    ("AB", defaultdict(lambda: "", {"AB": "C", "CB": "D"}), "ACB"),
    ("ABC", defaultdict(lambda: "", {"AB": "C", "BC": "D"}), "ACBDC"),
])
def test_polymer_insertion(polymer, insertion_rules, expected):
    assert polymer_insertion(polymer=polymer, insertion_rules=insertion_rules) == expected


AOC_EXAMPLE_INPUT = """NNCB

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


def test_polymer_insertion_aoc_example():
    polymer = parse_polymer_template(AOC_EXAMPLE_INPUT)
    insertion_rules = parse_insertion_rules(AOC_EXAMPLE_INPUT)
    step_1_polymer = polymer_insertion(polymer=polymer, insertion_rules=insertion_rules)
    assert step_1_polymer == "NCNBCHB"
    step_2_polymer = polymer_insertion(polymer=step_1_polymer, insertion_rules=insertion_rules)
    assert step_2_polymer == "NBCCNBBBCBHCB"
    step_3_polymer = polymer_insertion(polymer=step_2_polymer, insertion_rules=insertion_rules)
    assert step_3_polymer == "NBBBCNCCNBBNBNBBCHBHHBCHB"
    step_4_polymer = polymer_insertion(polymer=step_3_polymer, insertion_rules=insertion_rules)
    assert step_4_polymer == "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"



def polymer_insertion(polymer: str, insertion_rules: Dict[str, str]):
    result = ""
    for i in range(len(polymer)):
        result += polymer[i]
        result += insertion_rules[polymer[i:i+2]]
    return result


def part_a(filepath: str):
    with open(filepath, "r") as file:
        pass


def part_b(filepath: str):
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    day = 14
    input_file = f"../puzzle_input/day{day}.txt"
    print(f"The answer to {day}A is: {part_a(input_file)}")
    print(f"The answer to {day}B is: {part_b(input_file)}")
