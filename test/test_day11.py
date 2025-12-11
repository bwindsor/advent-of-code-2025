import pytest
from day11.day11 import day11_part1_algorithm, day11_part2_algorithm


def test_day11_part1_full():
    test_input = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out""".replace("\r", "")
    expected_output = 5
    assert day11_part1_algorithm(test_input) == expected_output


def test_day7_part2_full():
    test_input = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out""".replace("\r", "")
    expected_output = 2
    assert day11_part2_algorithm(test_input) == expected_output
