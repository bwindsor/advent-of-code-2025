"""
https://adventofcode.com/2025/day/1#part2
Method 0x434C49434B is ascii "CLICK" in hex
"""

from typing import Iterable
import pathlib
import itertools
import collections

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


def pairwise_gather(data0: tuple[int, list], data1: tuple[int, list]) -> tuple[int, list]:
    relative_finish_0 = data0[0]
    relative_finish_1 = data1[0]
    v0 = data0[1]
    v1 = data1[1]

    # Shifted version, if d1_start is at 1, we want v1_shifted[1] = v1[0], v1_shifted[0] = v1[99]
    if relative_finish_0 != 0:
        v1_shifted = v1[-relative_finish_0:] + v1[:100-relative_finish_0]
    else:
        v1_shifted = v1

    assert len(v1_shifted) == 100

    relative_finish_combined = (relative_finish_0 + relative_finish_1) % 100
    v_combined = [a + b for a, b in zip(v0, v1_shifted)]

    return relative_finish_combined, v_combined


def iter_pairs(x):
    while True:
        try:
            x0 = next(x)
            x1 = next(x)
        except StopIteration:
            return
        yield x0, x1


def process_line(line: str):
    direction = 1 if line[0] == 'R' else -1
    distance = int(line[1:])

    full_laps = distance // 100
    rem = distance % 100

    visits = [full_laps] * 100

    if direction == 1:
        for i in range(rem):
            visits[i+1] += 1
    else:
        for i in range(rem):
            visits[100-i-1] += 1

    return (direction * distance) % 100, visits


def day1_part2_algorithm_parallel(input_lines: Iterable[str]) -> int:
    all_data = list(map(process_line, input_lines))

    # Gather in pairs
    while len(all_data) > 1:
        if len(all_data) % 2 != 0:
            all_data[-2] = pairwise_gather(all_data[-2], all_data[-1])
            all_data = all_data[:-1]
        all_data = [pairwise_gather(p1, p2) for p1, p2 in iter_pairs(iter(all_data))]

    # Or us itertools accumulate, this doesn't cut the data in half each time though
    # all_data = [collections.deque(itertools.accumulate(map(process_line, input_lines), pairwise_gather, initial=(0, [0] * 100)), maxlen=1)[0]]

    # Extract final result, based on us starting on 50
    zero_visits = all_data[0][1][50]
    return zero_visits


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        result = day1_part2_algorithm_parallel(f)

    return result


if __name__ == "__main__":
    print(main())
