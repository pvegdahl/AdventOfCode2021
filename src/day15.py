import functools
import heapq
import sys
from collections import defaultdict
from typing import List, Tuple, Dict, Set

import pytest

from src.aoc_helpers import parse_digit_matrix, Point, list_matrix_to_tuple_matrix


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
def aoc_example_matrix(aoc_example_text) -> Tuple[Tuple[int, ...], ...]:
    return list_matrix_to_tuple_matrix(parse_digit_matrix(aoc_example_text))


@pytest.mark.parametrize(
    "starting_point, expected",
    [
        (Point(9, 9), 0),
        (Point(9, 8), 1),
        (Point(8, 8), 2),
        (Point(9, 7), 2),
        (Point(7, 9), 9),
        (Point(8, 7), 4),
        (Point(0, 0), 40),
    ],
)
def test_find_risk_of_best_route(starting_point, expected, aoc_example_matrix):
    assert (
        find_risk_of_best_route(
            matrix=aoc_example_matrix, starting_point=starting_point
        )
        == expected
    )


@functools.cache
def find_risk_of_best_route(
    matrix: Tuple[Tuple[int, ...], ...], starting_point: Point
) -> int:
    destination_point = Point(x=len(matrix) - 1, y=len(matrix[-1]) - 1)
    if starting_point == destination_point:
        return 0

    candidate_points = get_candidate_points(matrix=matrix, current_point=starting_point)
    lowest_score = 1e1000
    for point in candidate_points:
        score = matrix[point.x][point.y] + find_risk_of_best_route(
            matrix=matrix, starting_point=point
        )
        if score < lowest_score:
            lowest_score = score
    return lowest_score


def get_candidate_neighbors(node: Point, unvisited_nodes: Set[Point]) -> List[Point]:
    x = node.x
    y = node.y
    return [
        neighbor
        for neighbor in [
            Point(x + 1, y),
            Point(x - 1, y),
            Point(x, y + 1),
            Point(x, y - 1),
        ]
        if neighbor in unvisited_nodes
    ]


def test_dijkstra(aoc_example_matrix):
    assert dijkstra(aoc_example_matrix)[Point(9, 9)] == 40
    assert (
        dijkstra(build_multiplied_matrix(matrix=aoc_example_matrix, multiplier=5))[
            Point(49, 49)
        ]
        == 315
    )


def dijkstra(matrix: Tuple[Tuple[int, ...], ...]) -> Dict[Point, int]:
    unvisited_nodes = set()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            unvisited_nodes.add(Point(i, j))
    result = defaultdict(lambda: 1000000000000000)
    result[Point(0, 0)] = 0
    available_to_visit_heap = []
    heapq.heappush(available_to_visit_heap, (0, Point(0, 0)))

    while unvisited_nodes:
        current_node_score, current_node = heapq.heappop(available_to_visit_heap)
        if current_node in unvisited_nodes:
            unvisited_nodes.remove(current_node)
            candidates = get_candidate_neighbors(
                node=current_node, unvisited_nodes=unvisited_nodes
            )
            for node in candidates:
                score = min(current_node_score + matrix[node.x][node.y], result[node])
                result[node] = score
                heapq.heappush(available_to_visit_heap, (score, node))
    return result


def get_candidate_points(
    matrix: Tuple[Tuple[int, ...], ...], current_point: Point
) -> List[Point]:
    result = []
    if (current_point.x + 1) < len(matrix):
        result.append(Point(x=current_point.x + 1, y=current_point.y))
    if (current_point.y + 1) < len(matrix[0]):
        result.append(Point(x=current_point.x, y=current_point.y + 1))
    return result


@pytest.mark.parametrize(
    "matrix, multiplier, expected",
    [
        (((1,),), 1, ((1,),)),
        (((1,),), 2, ((1, 2), (2, 3))),
        (
            ((1, 2), (3, 4)),
            2,
            (
                (1, 2, 2, 3),
                (3, 4, 4, 5),
                (2, 3, 3, 4),
                (4, 5, 5, 6),
            ),
        ),
        (((8,),), 3, ((8, 9, 1), (9, 1, 2), (1, 2, 3))),
    ],
)
def test_build_multiplied_matrix(matrix, multiplier, expected):
    assert build_multiplied_matrix(matrix=matrix, multiplier=multiplier) == expected


def build_multiplied_matrix(
    matrix: Tuple[Tuple[int, ...], ...], multiplier: int
) -> Tuple[Tuple[int, ...], ...]:
    list_matrix = []
    for i in range(multiplier):
        for row in matrix:
            new_row = []
            for j in range(multiplier):
                new_row.extend([weird_mod_ten(x + i + j) for x in row])
            list_matrix.append(new_row)
    return list_matrix_to_tuple_matrix(list_matrix)


def weird_mod_ten(x: int) -> int:
    result = x
    while result > 9:
        result -= 9
    return result


def test_find_best_path_on_multiplied_matrix(aoc_example_matrix):
    assert find_best_path_on_multiplied_matrix(aoc_example_matrix) == 315


def find_best_path_on_multiplied_matrix(matrix: Tuple[Tuple[int, ...], ...]) -> int:
    multiplied_matrix = build_multiplied_matrix(matrix=matrix, multiplier=5)
    return dijkstra(matrix=multiplied_matrix)[Point(499, 499)]


def part_a(filepath: str):
    with open(filepath, "r") as file:
        matrix = list_matrix_to_tuple_matrix(parse_digit_matrix(file.read()))
    return find_risk_of_best_route(matrix=matrix, starting_point=Point(0, 0))


def part_b(filepath: str):
    with open(filepath, "r") as file:
        matrix = list_matrix_to_tuple_matrix(parse_digit_matrix(file.read()))
    return find_best_path_on_multiplied_matrix(matrix)


if __name__ == "__main__":
    day = 15
    input_file = f"../puzzle_input/day{day}.txt"
    print(f"The answer to {day}A is: {part_a(input_file)}")
    print(f"The answer to {day}B is: {part_b(input_file)}")
