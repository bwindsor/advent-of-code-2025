"""
https://adventofcode.com/2025/day/7
"""
import pathlib


def day7_part1_algorithm(input_str: str) -> int:
    lines = input_str.split('\n')
    beams = [1 if c == "S" else 0 for c in lines[0]]
    splits = 0
    for line in lines[1:]:
        for i, c in enumerate(line):
            if c == "^" and beams[i] == 1:
                splits += 1
                beams[i-1] = 1
                beams[i] = 0
                beams[i+1] = 1
    return splits


def day7_part2_algorithm(input_str: str) -> int:
    lines = input_str.split('\n')
    counts = [1 if c == "S" else 0 for c in lines[0]]
    for line in lines[1:]:
        for i, c in enumerate(line):
            if c == "^" and counts[i] > 0:
                counts[i-1] += counts[i]
                counts[i+1] += counts[i]
                counts[i] = 0
    return sum(counts)


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        data = f.read().strip()
    result = day7_part2_algorithm(data)

    return result


if __name__ == "__main__":
    print(main())
