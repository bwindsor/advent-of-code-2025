"""
https://adventofcode.com/2025/day/1#part2
Method 0x434C49434B is ascii "CLICK" in hex
"""

from typing import Iterable
import pathlib
import itertools

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


def pairwise_gather(relative_finish_0: int, relative_finish_1: int, v0: list, v1: list) -> tuple[int, list]:

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


def day1_part2_algorithm_parallel(input_lines: Iterable[str]) -> int:
    data = [[1 if line[0] == 'R' else -1, int(line[1:])] for line in input_lines]
    all_data = []
    for d in data:
        distance = d[1]

        visits = [0] * 100
        full_laps = distance // 100
        rem = distance % 100

        for i in range(100):
            visits[i] += full_laps
        if d[0] == 1:
            for i in range(rem):
                visits[i+1] += 1
        else:
            for i in range(rem):
                visits[100-i-1] += 1
        all_data.append(((d[0] * d[1]) % 100, visits))

    # Gather in pairs
    while len(all_data) > 1:
        if len(all_data) % 2 != 0:
            all_data[-2] = pairwise_gather(all_data[-2][0], all_data[-1][0], all_data[-2][1], all_data[-1][1])
            all_data = all_data[:-1]
        all_data = [pairwise_gather(p1[0], p2[0], p1[1], p2[1]) for p1, p2 in iter_pairs(iter(all_data))]

    result_relative_finish = all_data[0][0]
    result_visits = all_data[0][1]

    visits_shifted = result_visits[-50:] + result_visits[50:]  # Starts on 50
    zero_visits = visits_shifted[0]
    return zero_visits


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        result = day1_part2_algorithm_parallel(f)

    return result


if __name__ == "__main__":
    print(main())
