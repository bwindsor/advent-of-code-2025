import pytest
from day2.day2 import day2_part1_algorithm


def dumb_algorithm(input_str: str) -> int:
    total = 0
    ranges = [[int(x) for x in r.split("-")] for r in input_str.split(",")]
    for r_start, r_end in ranges:
        for x in range(r_start, r_end+1):
            x_str = str(x)
            if len(x_str) % 2 == 0:
                part_len = len(x_str) // 2
                if x_str[:part_len] == x_str[part_len:]:
                    total += x
    return total


def test_day2_full():
    test_input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
    expected_output = 1227775554
    assert day2_part1_algorithm(test_input) == expected_output
    assert dumb_algorithm(test_input) == expected_output


@pytest.mark.parametrize("input_str, expected_output", [
    ("11-22", 33),
    ("95-115", 99),
    ("998-1012", 1010),
    ("1188511880-1188511890", 1188511885),
    ("222220-222224", 222222),
    ("1698522-1698528", 0),
    ("446443-446449", 446446),
    ("38593856-38593862", 38593859),
    ("565653-565659", 0),
    ("824824821-824824827", 0),
    ("2121212118-2121212124", 0),
    ("959516-960960", 959959+960960),
    ("959516-960961", 959959+960960),
    ("959516-960959", 959959),
    ("959959-960960", 959959+960960),
    ("959958-960960", 959959+960960),
    ("959960-960960", 960960),
    ("1-11", 11),
    ("123-999", 0),
    ("4-18", 11),
    ("1-30", 11+22),
])
def test_day2(input_str: str, expected_output: int):
    assert day2_part1_algorithm(input_str) == expected_output
    assert dumb_algorithm(input_str) == expected_output


def test_find_failures():
    for x in range(1000):
        input_str = f"1-{x}"
        assert day2_part1_algorithm(input_str) == dumb_algorithm(input_str), f"Failed for x = {x}"
