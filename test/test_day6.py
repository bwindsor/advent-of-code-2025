import pytest
from day6.day6 import day6_part1_algorithm, day6_part2_algorithm, get_line_len
import tempfile
import pathlib


@pytest.mark.parametrize("line_len", [
    1, 100, 1023, 1024, 1025, 2047, 2048, 2049, 10000
])
def test_get_line_len(line_len: int):
    with tempfile.TemporaryDirectory() as td:
        with open(pathlib.Path(td) / "input.txt", "wb") as f:
            f.write(b"0" * (line_len - 1))
            f.write(b'\n')
            f.write(b"1" * (line_len - 1))
            f.write(b'\n\n')
        with open(pathlib.Path(td) / "input.txt", "rb") as f:
            assert get_line_len(f) == line_len


def test_day6_part1_full():
    expected_output = 4277556
    with tempfile.TemporaryDirectory() as td:
        with open(pathlib.Path(td) / "input.txt", "wb") as f:
            f.write(b"123 328  51 64 \n")
            f.write(b" 45 64  387 23 \n")
            f.write(b"  6 98  215 314\n")
            f.write(b"*   +   *   +  \n\n")
        assert day6_part1_algorithm(str(pathlib.Path(td) / "input.txt")) == expected_output


def test_day6_part1():
    expected_output = 668 + 8161 + 592
    with tempfile.TemporaryDirectory() as td:
        with open(pathlib.Path(td) / "input.txt", "wb") as f:
            f.write(b"668 8161 592\n")
            f.write(b"+   +    +  \n\n")
        assert day6_part1_algorithm(str(pathlib.Path(td) / "input.txt")) == expected_output


def test_day3_part2_full():
    expected_output = 3263827
    with tempfile.TemporaryDirectory() as td:
        with open(pathlib.Path(td) / "input.txt", "wb") as f:
            f.write(b"123 328  51 64 \n")
            f.write(b" 45 64  387 23 \n")
            f.write(b"  6 98  215 314\n")
            f.write(b"*   +   *   +  \n\n")
        assert day6_part2_algorithm(str(pathlib.Path(td) / "input.txt")) == expected_output
