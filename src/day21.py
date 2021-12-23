from typing import NamedTuple

import pytest


class GameState(NamedTuple):
    roll_count: int = 0
    position_one: int = 1


@pytest.mark.parametrize("initial_game_state, expected_roll_count", [
    (GameState(roll_count=0), 3),
    (GameState(roll_count=3), 6),
    (GameState(roll_count=369), 372),
])
def test_roll_count_updated(initial_game_state, expected_roll_count):
    assert one_turn(initial_game_state).roll_count == expected_roll_count


@pytest.mark.parametrize("initial_game_state, expected_position_one", [
    (GameState(position_one=1, roll_count=0), 7),
    (GameState(position_one=10, roll_count=0), 6),
    (GameState(position_one=10, roll_count=10), 6),
    (GameState(position_one=10, roll_count=1000), 6),
    (GameState(position_one=3, roll_count=123), 8),
])
def test_position_one_updated(initial_game_state, expected_position_one):
    assert one_turn(initial_game_state).position_one == expected_position_one


def one_turn(initial_game_state: GameState) -> GameState:
    new_position_one = calculate_new_position_one(initial_game_state)
    return GameState(roll_count=initial_game_state.roll_count+3, position_one=new_position_one)


def calculate_new_position_one(initial_game_state):
    roll_total = 3 * initial_game_state.roll_count + 6
    new_position_one = special_mod10(initial_game_state.position_one + roll_total)
    return new_position_one


def special_mod10(number: int) -> int:
    return (number-1) % 10 + 1


def part_a(filepath: str):
    with open(filepath, "r") as file:
        pass


def part_b(filepath: str):
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    day = 21
    input_file = f"../puzzle_input/day{day}.txt"
    print(f"The answer to {day}A is: {part_a(input_file)}")
    print(f"The answer to {day}B is: {part_b(input_file)}")
