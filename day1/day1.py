"""
https://adventofcode.com/2025/day/1
"""
from typing import Iterable
import pathlib


def day1_algorithm(input_lines: Iterable[str]) -> int:
    position = 50
    result = 0

    for line in input_lines:
        direction = 1 if line[0] == 'R' else -1
        distance = int(line[1:])
        position = (position + direction * distance) % 100
        if position == 0:
            result += 1

    return result


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        result = day1_algorithm(f)

    return result


if __name__ == "__main__":
    print(main())
