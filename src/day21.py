import functools
from collections import defaultdict
from typing import NamedTuple, Tuple, List, Dict

import pytest


class PlayerState(NamedTuple):
    position: int = 1
    score: int = 0

    def one_quantum_roll(self) -> List["PlayerState"]:
        result = []
        for roll in (1, 2, 3):
            new_pos = special_mod10(self.position + roll)
            new_score = self.score + new_pos
            result.append(PlayerState(position=new_pos, score=new_score))
        return result

    def one_quantum_turn(self) -> Dict["PlayerState", int]:
        result = defaultdict(lambda: 0)
        for roll, count in roll_histogram().items():
            player_state = self.one_roll(roll)
            result[player_state] += count
        return result

    def one_roll(self, roll: int) -> "PlayerState":
        new_pos = special_mod10(self.position + roll)
        new_score = self.score + new_pos
        return PlayerState(position=new_pos, score=new_score)


@pytest.mark.parametrize("player_state, expected", [
    (PlayerState(), [PlayerState(position=2, score=2), PlayerState(position=3, score=3), PlayerState(position=4, score=4)]),
    (PlayerState(position=9, score=51),
     [PlayerState(position=10, score=61), PlayerState(position=1, score=52), PlayerState(position=2, score=53)]),
])
def test_one_quantum_roll(player_state, expected):
    assert player_state.one_quantum_roll() == expected


@functools.cache
def roll_histogram():
    result = {0: 1}
    for _ in range(3):
        old_result = result
        result = defaultdict(lambda: 0)
        for key, value in old_result.items():
            for i in (1, 2, 3):
                new_key = key + i
                result[new_key] += value
    return result


def test_roll_histogram():
    assert roll_histogram() == {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


def test_one_quantum_turn():
    assert PlayerState(position=5, score=0).one_quantum_turn() == {
        PlayerState(position=8, score=8): 1,
        PlayerState(position=9, score=9): 3,
        PlayerState(position=10, score=10): 6,
        PlayerState(position=1, score=1): 7,
        PlayerState(position=2, score=2): 6,
        PlayerState(position=3, score=3): 3,
        PlayerState(position=4, score=4): 1,
    }


class GameState(NamedTuple):
    roll_count: int = 0
    player_states: Tuple[PlayerState, ...] = (PlayerState(),)
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
        pos_one: int = 1,
        score_one: int = 0,
        roll_count: int = 0,
        player_turn: int = 0,
    ):
        return GameState(
            roll_count=roll_count,
            player_turn=player_turn,
            player_states=(
                PlayerState(position=pos_zero, score=score_zero),
                PlayerState(position=pos_one, score=score_one),
            ),
        )

    def game_score(self) -> int:
        min_score = min(player.score for player in self.player_states)
        return min_score * self.roll_count


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
        player_turn=calculate_new_player_turn(initial_game_state),
    )


def calculate_new_roll_count(initial_game_state):
    return initial_game_state.roll_count + 3


def calculate_new_player_states(game_state: GameState) -> Tuple[PlayerState]:
    return tuple(
        calculate_new_player_state(game_state, i)
        for i in range(len(game_state.player_states))
    )


def calculate_new_player_turn(game_state: GameState) -> int:
    return (game_state.player_turn + 1) % 2


def calculate_new_player_state(game_state: GameState, player_id: int) -> PlayerState:
    if game_state.player_turn == player_id:
        player_state = game_state.player_states[player_id]
        new_position = calculate_new_position(
            current_position=player_state.position, roll_count=game_state.roll_count
        )
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


def run_turns_until_score(game_state: GameState, target_score: int) -> GameState:
    while not score_reached(game_state, target_score):
        game_state = one_turn(game_state)
    return game_state


def score_reached(game_state, target_score):
    for player in game_state.player_states:
        if player.score >= target_score:
            return True
    return False


def test_run_turns_until_score():
    game_state = GameState(
        player_states=(PlayerState(position=4), PlayerState(position=8))
    )
    final_state = run_turns_until_score(game_state, 1000)
    assert final_state == GameState(
        roll_count=993,
        player_turn=1,
        player_states=(
            PlayerState(position=10, score=1000),
            PlayerState(position=3, score=745),
        ),
    )


@pytest.mark.parametrize(
    "game_state, expected",
    [
        (GameState(), 0),
        (GameState.factory(score_zero=3, score_one=5, roll_count=4), 12),
        (
            GameState(
                roll_count=993,
                player_turn=1,
                player_states=(
                    PlayerState(position=10, score=1000),
                    PlayerState(position=3, score=745),
                ),
            ),
            739785,
        ),
    ],
)
def test_game_score(game_state, expected):
    assert game_state.game_score() == expected


def aoc_input() -> GameState:
    return GameState.factory(pos_zero=10, pos_one=8)


def part_a():
    final_game_state = run_turns_until_score(game_state=aoc_input(), target_score=1000)
    return final_game_state.game_score()


def part_b():
    pass


if __name__ == "__main__":
    day = 21
    print(f"The answer to {day}A is: {part_a()}")
    print(f"The answer to {day}B is: {part_b()}")
