"""
https://adventofcode.com/2025/day/5
"""
import pathlib


def day5_part1_algorithm(input_str: str) -> int:
    sections = input_str.split('\n\n')
    assert len(sections) == 2
    ranges = [tuple(int(x) for x in s.split('-')) for s in sections[0].split('\n')]
    ranges.sort()
    for i in range(len(ranges)-1):
        r0 = ranges[i]
        r1 = ranges[i+1]
        if r1[0] <= r0[1]:  # There is overlap
            if r1[1] <= r0[1]:  # r1 is a subrange of r0
                ranges[i+1] = ranges[i]
            else:
                # Merge
                ranges[i+1] = r0[0], r1[1]
            ranges[i] = None
    ranges = list(filter(lambda x: x is not None, ranges))

    # Ranges is now sorted and non-overlapping
    available_ids = sorted(int(x) for x in sections[1].split('\n'))

    range_idx = 0
    result = 0
    for available_id in available_ids:
        while range_idx < len(ranges) - 1 and available_id > ranges[range_idx][1]:
            range_idx += 1
        if ranges[range_idx][0] <= available_id <= ranges[range_idx][1]:
            result += 1

    return result


def day5_part2_algorithm(input_str: str) -> int:
    sections = input_str.split('\n\n')
    assert len(sections) == 2
    ranges = [tuple(int(x) for x in s.split('-')) for s in sections[0].split('\n')]
    ranges.sort()
    for i in range(len(ranges) - 1):
        r0 = ranges[i]
        r1 = ranges[i + 1]
        if r1[0] <= r0[1]:  # There is overlap
            if r1[1] <= r0[1]:  # r1 is a subrange of r0
                ranges[i + 1] = ranges[i]
            else:
                # Merge
                ranges[i + 1] = r0[0], r1[1]
            ranges[i] = None

    result = 0
    for r in ranges:
        if r is not None:
            result += r[1] - r[0] + 1

    return result


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        data = f.read().replace('\r', '')
    result = day5_part2_algorithm(data)

    return result


if __name__ == "__main__":
    print(main())
