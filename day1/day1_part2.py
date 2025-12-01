"""
https://adventofcode.com/2025/day/1#part2
Method 0x434C49434B is ascii "CLICK" in hex
"""

from typing import Iterable
import pathlib
import math
from numba import cuda
import numpy as np


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


def pairwise_gather(data0: list[int], data1: list[int]) -> list[int]:
    result = [0] * 101
    for i in range(101):
        if i < 100:
            result[i] = data0[i] + data1[(i - data0[100]) % 100]
        else:
            result[i] = (data0[i] + data1[i]) % 100

    return result


def iter_pairs(x):
    while True:
        try:
            x0 = next(x)
            x1 = next(x)
        except StopIteration:
            return
        yield x0, x1


def parse_line(line: str):
    direction = 1 if line[0] == 'R' else -1
    distance = int(line[1:])
    return direction, distance


def process_line(input_data: tuple[int,int]):
    direction, distance = input_data

    data = [0] * 101
    for i in range(101):
        if i < 100:
            data[i] = distance // 100  # Number of full laps
            rem = distance % 100
            if direction == 1 and 0 < i <= rem:
                data[i] += 1
            elif direction == -1 and i >= 100-rem:
                data[i] += 1
        else:
            data[i] = (direction * distance) % 100

    return data


def next_pow2_exponent(n: int) -> int:
    if n <= 0:
        return 1

    # If n is already a power of two, math.log2(n) will be an integer.
    # log2(n) gives the exponent.
    exponent = math.ceil(math.log2(n))
    return exponent


def day1_part2_algorithm_parallel(input_lines: Iterable[str]) -> int:
    data_for_gpu = list(map(parse_line, input_lines))
    # Make it a power of 2
    exponent = next_pow2_exponent(len(data_for_gpu))
    desired_length = 2 ** exponent
    new_items_required = desired_length - len(data_for_gpu)
    data_for_gpu.extend([(1,0)] * new_items_required)

    # TODO send data_for_gpu to the GPU

    # Run in parallel, can be done on GPU
    all_data = list(map(process_line, data_for_gpu))

    # Gather in pairs, can be done on GPU. It's a power of 2 so this will always work
    for i_gather in range(exponent):
        all_data = [pairwise_gather(p1, p2) for p1, p2 in iter_pairs(iter(all_data))]

    assert len(all_data) == 1

    # Retrieve final result, based on starting at position 50
    zero_visits = all_data[0][50]
    return zero_visits


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        result = day1_part2_algorithm_parallel(f)

    return result


if __name__ == "__main__":
    print(main())
