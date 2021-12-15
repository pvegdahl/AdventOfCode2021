from typing import List

import pytest

from src.aoc_helpers import parse_digit_matrix, Point


@pytest.fixture
def aoc_example_text() -> str:
    return """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


@pytest.fixture
def aoc_example_matrix(aoc_example_text) -> List[List[int]]:
    return parse_digit_matrix(aoc_example_text)


@pytest.mark.parametrize("starting_point, expected", [
    (Point(9, 9), 0),
    (Point(9, 8), 1),
    (Point(8, 8), 2),
    (Point(9, 7), 2),
    (Point(7, 9), 9),
    (Point(8, 7), 4),
    (Point(0, 0), 40),
])
def test_find_risk_of_best_route(starting_point, expected, aoc_example_matrix):
    assert find_risk_of_best_route(matrix=aoc_example_matrix, starting_point=starting_point) == expected


def find_risk_of_best_route(matrix: List[List[int]], starting_point: Point) -> int:
    destination_point = Point(x=len(matrix)-1, y=len(matrix[-1])-1)
    if starting_point == destination_point:
        return 0

    candidate_points = get_candidate_points(matrix=matrix, current_point=starting_point)
    lowest_score = 1e1000
    for point in candidate_points:
        score = matrix[point.x][point.y] + find_risk_of_best_route(matrix=matrix, starting_point=point)
        if score < lowest_score:
            lowest_score = score
    return lowest_score


def get_candidate_points(matrix: List[List[int]], current_point: Point) -> List[Point]:
    result = []
    if (current_point.x + 1) < len(matrix):
        result.append(Point(x=current_point.x + 1, y=current_point.y))
    if (current_point.y + 1) < len(matrix[0]):
        result.append(Point(x=current_point.x, y=current_point.y + 1))
    return result



def part_a(filepath: str):
    with open(filepath, "r") as file:
        pass


def part_b(filepath: str):
    with open(filepath, "r") as file:
        pass


if __name__ == "__main__":
    day = 15
    input_file = f"../puzzle_input/day{day}.txt"
    print(f"The answer to {day}A is: {part_a(input_file)}")
    print(f"The answer to {day}B is: {part_b(input_file)}")
