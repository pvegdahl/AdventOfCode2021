from typing import NamedTuple, Tuple

import pytest


class PlayerState(NamedTuple):
    position: int = 1
    score: int = 0


class GameState(NamedTuple):
    roll_count: int = 0
    player_states: Tuple[PlayerState] = PlayerState(),
    the_position_one: int = 1
    the_score_one: int = 0
    player_turn: int = 1

    def position_one(self):
        return self.the_position_one

    def score_one(self):
        return self.the_score_one

    @classmethod
    def factory(cls, pos_one: int = 1, score_one: int = 0, roll_count: int = 0, player_turn: int = 1):
        return GameState(the_position_one=pos_one, the_score_one=score_one, roll_count=roll_count, player_turn=player_turn, player_states=(PlayerState(position=pos_one, score=score_one)))


@pytest.mark.parametrize(
    "initial_game_state, expected",
    [
        (GameState.factory(roll_count=0), 3),
        (GameState.factory(roll_count=3), 6),
        (GameState.factory(roll_count=369), 372),
    ],
)
def test_roll_count_updated(initial_game_state, expected):
    assert one_turn(initial_game_state).roll_count == expected


@pytest.mark.parametrize(
    "initial_game_state, expected",
    [
        (GameState.factory(pos_one=1, roll_count=0), 7),
        (GameState.factory(pos_one=10, roll_count=0), 6),
        (GameState.factory(pos_one=10, roll_count=10), 6),
        (GameState.factory(pos_one=10, roll_count=1000), 6),
        (GameState.factory(pos_one=3, roll_count=123), 8),
    ],
)
def test_position_one_updated(initial_game_state, expected):
    assert one_turn(initial_game_state).position_one() == expected


@pytest.mark.parametrize(
    "initial_game_state, expected",
    [
        (GameState.factory(pos_one=1, roll_count=0, score_one=0), 7),
        (GameState.factory(pos_one=1, roll_count=0, score_one=10), 17),
        (GameState.factory(pos_one=3, roll_count=123, score_one=123), 131),
    ],
)
def test_score_one_updated(initial_game_state, expected):
    assert one_turn(initial_game_state).score_one() == expected


def test_player_one_not_updated_on_player_two_turn():
    initial_game_state = GameState.factory(player_turn=2)
    next_game_state = one_turn(initial_game_state)
    assert next_game_state.score_one() == initial_game_state.score_one()
    assert next_game_state.position_one() == initial_game_state.position_one()


@pytest.mark.parametrize(
    "initial_player_turn, expected",
    [
        (1, 2),
        (2, 1),
    ],
)
def test_turn_alternates(initial_player_turn, expected):
    assert one_turn(GameState.factory(player_turn=initial_player_turn)).player_turn == expected


def one_turn(initial_game_state: GameState) -> GameState:
    if initial_game_state.player_turn == 1:
        new_position_one = calculate_new_position_one(initial_game_state)
        new_score_one = initial_game_state.score_one() + new_position_one
        return GameState.factory(
            roll_count=initial_game_state.roll_count + 3,
            pos_one=new_position_one,
            score_one=new_score_one,
            player_turn=2,
        )
    else:
        return initial_game_state._replace(player_turn=1)


def calculate_new_position_one(initial_game_state):
    roll_total = 3 * initial_game_state.roll_count + 6
    new_position_one = special_mod10(initial_game_state.position_one() + roll_total)
    return new_position_one


def special_mod10(number: int) -> int:
    return (number - 1) % 10 + 1


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
