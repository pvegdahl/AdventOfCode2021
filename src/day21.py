from typing import NamedTuple

import pytest


class GameState(NamedTuple):
    roll_count: int = 0


@pytest.mark.parametrize("initial_game_state, expected_roll_count", [
    (GameState(roll_count=0), 3),
    (GameState(roll_count=3), 6),
    (GameState(roll_count=369), 372),
])
def test_roll_count_updated(initial_game_state, expected_roll_count):
    assert one_turn(initial_game_state).roll_count == expected_roll_count


def one_turn(initial_game_state: GameState) -> GameState:
    return GameState(roll_count=initial_game_state.roll_count+3)


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
