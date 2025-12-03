import pytest
from day3.day3 import day3_part1_algorithm, day3_part2_algorithm


def test_day3_part1_full():
    test_input = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111",
    ]
    expected_output = 357
    assert day3_part1_algorithm(test_input) == expected_output


@pytest.mark.parametrize("input_list, expected_output", [
    (["987654321111111"], 98),
    (["811111111111119"], 89),
    (["234234234234278"], 78),
    (["818181911112111"], 92),
])
def test_day3_part1(input_list: list[str], expected_output: int):
    assert day3_part1_algorithm(input_list) == expected_output


def test_day3_part2_full():
    test_input = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111",
    ]
    expected_output = 3121910778619
    assert day3_part2_algorithm(test_input) == expected_output


@pytest.mark.parametrize("input_list, expected_output", [
    (["987654321111111"], 987654321111),
    (["811111111111119"], 811111111119),
    (["234234234234278"], 434234234278),
    (["818181911112111"], 888911112111),
])
def test_day3_part2(input_list: list[str], expected_output: int):
    assert day3_part2_algorithm(input_list) == expected_output