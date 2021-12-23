from typing import NamedTuple, Tuple

import pytest


class PlayerState(NamedTuple):
    position: int = 1
    score: int = 0


class GameState(NamedTuple):
    roll_count: int = 0
    player_states: Tuple[PlayerState] = (PlayerState(),)
    player_turn: int = 0

    def position_zero(self):
        return self.player_states[0].position

    def score_zero(self):
        return self.player_states[0].score

    @classmethod
    def factory(
        cls,
        pos_zero: int = 1,
        score_zero: int = 0,
        roll_count: int = 0,
        player_turn: int = 0,
    ):
        return GameState(
            roll_count=roll_count,
            player_turn=player_turn,
            player_states=(PlayerState(position=pos_zero, score=score_zero),),
        )


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
        (GameState.factory(pos_zero=1, roll_count=0), 7),
        (GameState.factory(pos_zero=10, roll_count=0), 6),
        (GameState.factory(pos_zero=10, roll_count=10), 6),
        (GameState.factory(pos_zero=10, roll_count=1000), 6),
        (GameState.factory(pos_zero=3, roll_count=123), 8),
    ],
)
def test_position_zero_updated(initial_game_state, expected):
    assert one_turn(initial_game_state).position_zero() == expected


@pytest.mark.parametrize(
    "initial_game_state, expected",
    [
        (GameState.factory(pos_zero=1, roll_count=0, score_zero=0), 7),
        (GameState.factory(pos_zero=1, roll_count=0, score_zero=10), 17),
        (GameState.factory(pos_zero=3, roll_count=123, score_zero=123), 131),
    ],
)
def test_score_zero_updated(initial_game_state, expected):
    assert one_turn(initial_game_state).score_zero() == expected


def test_player_zero_not_updated_on_player_one_turn():
    initial_game_state = GameState.factory(player_turn=1)
    next_game_state = one_turn(initial_game_state)
    assert next_game_state.player_states[0] == initial_game_state.player_states[0]


def test_player_one_not_updated_on_player_zero_turn():
    initial_game_state = GameState(player_states=(PlayerState(), PlayerState()))
    next_game_state = one_turn(initial_game_state)
    assert next_game_state.player_states[1] == initial_game_state.player_states[1]


@pytest.mark.parametrize(
    "initial_player_turn, expected",
    [
        (0, 1),
        (1, 0),
    ],
)
def test_turn_alternates(initial_player_turn, expected):
    assert (
        one_turn(GameState.factory(player_turn=initial_player_turn)).player_turn
        == expected
    )


def one_turn(initial_game_state: GameState) -> GameState:
    return GameState(
        roll_count=calculate_new_roll_count(initial_game_state),
        player_states=calculate_new_player_states(initial_game_state),
        player_turn=calculate_new_player_turn(initial_game_state))


def calculate_new_roll_count(initial_game_state):
    return initial_game_state.roll_count + 3


def calculate_new_player_states(game_state: GameState) -> Tuple[PlayerState]:
    return tuple(calculate_new_player_state(game_state, i) for i in range(len(game_state.player_states)))


def calculate_new_player_turn(game_state: GameState) -> int:
    return (game_state.player_turn + 1) % 2


def calculate_new_player_state(game_state: GameState, player_id: int) -> PlayerState:
    if game_state.player_turn == player_id:
        player_state = game_state.player_states[player_id]
        new_position = calculate_new_position(current_position=player_state.position, roll_count=game_state.roll_count)
        new_score = player_state.score + new_position
        return PlayerState(position=new_position, score=new_score)
    else:
        return game_state.player_states[player_id]


def calculate_new_position(current_position: int, roll_count: int):
    roll_total = 3 * roll_count + 6
    new_position = special_mod10(current_position + roll_total)
    return new_position


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
