import pytest
from day4.day4 import day4_part1_algorithm, day4_part2_algorithm


def test_day4_part1_full():
    test_input = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
    expected_output = 13
    assert day4_part1_algorithm(test_input) == expected_output


def test_day4_part2_full():
    test_input = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
    expected_output = 43
    assert day4_part2_algorithm(test_input) == expected_output
