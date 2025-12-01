"""
https://adventofcode.com/2025/day/1#part2
Method 0x434C49434B is ascii "CLICK" in hex
"""

from typing import Iterable
import pathlib


def day1_part2_algorithm(input_lines: Iterable[str]) -> int:
    position = 50
    result = 0

    for line in input_lines:
        direction = 1 if line[0] == 'R' else -1
        distance = int(line[1:])

        # For direction left, reflect the dial so everything is like a right rotation, then we only have one case to deal with
        if direction == -1:
            position = (100 - position) % 100

        position = position + distance
        zero_passes = position // 100  # Gives correct answer for R rotations
        position = position % 100

        if direction == -1:
            position = (100 - position) % 100

        result += zero_passes

    return result


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        result = day1_part2_algorithm(f)

    return result


if __name__ == "__main__":
    print(main())
