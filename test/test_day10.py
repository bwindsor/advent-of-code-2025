import pytest
from day10.day10 import day10_part1_algorithm, day10_part2_algorithm


def test_day10_part1_full():
    test_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}""".replace("\r", "")
    expected_output = 7
    assert day10_part1_algorithm(test_input) == expected_output


def test_day7_part2_full():
    test_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
    [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}""".replace("\r", "")
    expected_output = 40
    assert day10_part2_algorithm(test_input) == expected_output
