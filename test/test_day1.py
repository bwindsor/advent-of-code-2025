from day1.day1 import day1_algorithm
from day1.day1_part2 import day1_part2_algorithm
import pytest


@pytest.mark.parametrize("lines, expected_result", [
    (["L10"], 0),
    (["L50"], 1),
    (["R50"], 1),
    (["L10", "R160", "L100"], 2),
])
def test_day1(lines: list[str], expected_result: int) -> None:
    assert day1_algorithm(lines) == expected_result


@pytest.mark.parametrize("lines, expected_result", [
    (["L10"], 0),
    (["L50"], 1),
    (["R50"], 1),
    (["L10", "R160", "L100"], 3),
    (["L50", "R50"], 1),
    (["L50", "R50", "R50"], 2),
    (["L50", "L50"], 1),
    (["L50", "L99"], 1),
    (["L50", "L100"], 2),
])
def test_day1_part2(lines: list[str], expected_result: int) -> None:
    assert day1_part2_algorithm(lines) == expected_result
