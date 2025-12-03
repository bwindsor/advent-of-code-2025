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


def day3_part2_algorithm(input_lines: list[str]) -> int:
    total_joltage = 0
    for line in input_lines:
        j_out = [0] * 12
        line_joltages = [int(x) for x in line]

        for i, c in enumerate(line_joltages):
            for u in range(12):
                if c > j_out[u] and i < len(line)-(11-u):
                    j_out[u] = c
                    j_out[u+1:] = [0]*(11-u)
                    break

        for i, c in enumerate(j_out):
            total_joltage += c * 10**(11-i)

    return total_joltage


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        data = [x.strip() for x in f.read().strip().split('\n')]
    result = day3_part2_algorithm(data)

    return result


if __name__ == "__main__":
    print(main())
