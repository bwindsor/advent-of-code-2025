import pytest
from day5.day5 import day5_part1_algorithm, day5_part2_algorithm


def test_day5_part1_full():
    test_input = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
    expected_output = 3
    assert day5_part1_algorithm(test_input) == expected_output


@pytest.mark.parametrize("test_input, expected_output", [
    ("854928928779-8566391540121\n13378432871871-18518223043577\n\n25922854607\n96661323985\n412257224038\n551481293707\n2864620608008", 1),
    ("1-3\n3-5\n\n0\n1\n2\n3\n4\n5\n6\n7", 5),
    ("1-3\n4-5\n\n0\n1\n2\n3\n4\n5\n6\n7", 5),
    ("1-3\n5-5\n\n0\n1\n2\n3\n4\n5\n6\n7", 4),
    ("5-5\n1-3\n\n0\n1\n2\n3\n4\n5\n6\n7", 4),
    ("1-3\n5-5\n5-6\n\n0\n1\n2\n3\n4\n5\n6\n7", 5),
    ("1-3\n2-3\n5-5\n\n0\n1\n2\n3\n4\n5\n6\n7", 4),
    ("1-5\n2-3\n\n0\n1\n2\n3\n4\n5\n6\n7", 5),
])
def test_day5_part1(test_input, expected_output):
    assert day5_part1_algorithm(test_input) == expected_output


def test_day5_part2_full():
    test_input = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
    expected_output = 14
    assert day5_part2_algorithm(test_input) == expected_output
