"""
https://adventofcode.com/2025/day/2
"""
import pathlib
import math


def day2_part1_algorithm(ranges_str: str) -> int:
    ranges = [[int(x) for x in r.split("-")] for r in ranges_str.split(",")]

    total = 0
    for r_start, r_end in ranges:
        start_len = math.ceil(math.log10(r_start + 1))
        end_len = math.ceil(math.log10(r_end + 1))

        # Go through even length numbers in the range
        for i_len in range(start_len, end_len+1):
            if i_len % 2 == 0:
                x_start = max(r_start, 10 ** (i_len - 1))
                x_end = min(r_end, 10 ** i_len - 1)

                d = 10**(i_len // 2)
                repeated_part_start = x_start // d
                repeated_part_end = x_end // d
                rem_start = x_start % d
                rem_end = x_end % d

                # Special cases
                if repeated_part_start == repeated_part_end:
                    if rem_start <= repeated_part_start <= rem_end:
                        total += repeated_part_start * d + repeated_part_start
                    continue

                # If we are here, repeated_part_end > repeated_part_start
                # Initial case
                if repeated_part_start >= rem_start:
                    total += repeated_part_start * d + repeated_part_start

                # Intermediate cases
                for repeated_part in range(repeated_part_start+1, repeated_part_end):
                    total += repeated_part * d + repeated_part

                # Final case
                if repeated_part_end <= rem_end:
                    total += repeated_part_end * d + repeated_part_end

    return total


def _get_candidate(num_repeats: int, repeated_part_start: int, d: int):
    candidate = 0
    for p in range(0, num_repeats):
        candidate += repeated_part_start * d ** p
    return candidate


def day2_part2_algorithm(ranges_str: str) -> int:
    ranges = [[int(x) for x in r.split("-")] for r in ranges_str.split(",")]
    return day2_part2_algorithm_ranges(ranges)


def is_prime(x: int) -> bool:
    for i in range(2, int(math.sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True


def has_repeats(x: int, x_len: int) -> bool:
    for i_num_repeats in range(2, x_len + 1):
        if x_len % i_num_repeats == 0 and is_prime(i_num_repeats):
            d = 10 ** (x_len // i_num_repeats)
            repeated_part = x // (d ** (i_num_repeats - 1))
            candidate = _get_candidate(i_num_repeats, repeated_part, d)
            if x == candidate:
                return True
    return False


def day2_part2_algorithm_ranges(ranges: list[list[int]]) -> int:
    total = 0
    for r_start, r_end in ranges:
        start_len = math.ceil(math.log10(r_start + 1))
        end_len = math.ceil(math.log10(r_end + 1))

        # Go through each length of numbers in the range
        for i_len in range(start_len, end_len+1):
            x_start = max(r_start, 10 ** (i_len - 1))
            x_end = min(r_end, 10 ** i_len - 1)

            # Go through each possible number of repeats
            for i_num_repeats in range(2, i_len+1):
                if i_len % i_num_repeats == 0:
                    repeat_len = i_len // i_num_repeats
                    d = 10**(i_len // i_num_repeats)
                    repeated_part_start = x_start // (d**(i_num_repeats-1))
                    repeated_part_end = x_end // (d**(i_num_repeats-1))

                    # Special cases
                    if repeated_part_start == repeated_part_end and not has_repeats(repeated_part_start, repeat_len):
                        candidate = _get_candidate(i_num_repeats, repeated_part_start, d)
                        if x_start <= candidate <= x_end:
                            total += candidate
                        continue

                    # If we are here, repeated_part_end > repeated_part_start
                    # Initial case
                    if not has_repeats(repeated_part_start, repeat_len):
                        candidate = _get_candidate(i_num_repeats, repeated_part_start, d)
                        if candidate >= x_start:
                            total += candidate

                    # Intermediate cases
                    for repeated_part in range(repeated_part_start+1, repeated_part_end):
                        if not has_repeats(repeated_part, repeat_len):
                            candidate = _get_candidate(i_num_repeats, repeated_part, d)
                            total += candidate

                    # Final case
                    if not has_repeats(repeated_part_end, repeat_len):
                        candidate = _get_candidate(i_num_repeats, repeated_part_end, d)
                        if candidate <= x_end:
                            total += candidate

    return total


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        data = f.read().strip()
    result = day2_part2_algorithm(data)

    return result


if __name__ == "__main__":
    print(main())
