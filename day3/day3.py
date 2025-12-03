"""
https://adventofcode.com/2025/day/3
"""
import pathlib


def day3_part1_algorithm(input_lines: list[str]) -> int:
    total_joltage = 0
    for line in input_lines:
        j0 = "0"
        j1 = "0"
        for i, c in enumerate(line):
            if c > j0 and i < len(line)-1:
                j0 = c
                j1 = "0"
            elif c > j1:
                j1 = c

        total_joltage += int(j0) * 10 + int(j1)

    return total_joltage


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        data = [x.strip() for x in f.read().strip().split('\n')]
    result = day3_part1_algorithm(data)

    return result


if __name__ == "__main__":
    print(main())
