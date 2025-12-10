"""
https://adventofcode.com/2025/day/10
"""
import pathlib
import re
import itertools
import functools
import operator


def day10_part1_algorithm(input_str: str) -> int:
    """

    In binary if we store the current indicator pattern as bits, and the button effect as bits, this is what we see
    previous_value | button_effect | desired_output
    0 0 0
    0 1 1
    1 0 1
    1 1 0
    This is **xor**
    """

    lines = input_str.split('\n')
    matches = [re.match(r"\[([.#]+)] ((\([,\d]+\) )+)\{([,\d]+)\}", line) for line in lines]
    indicator_patterns = [sum(1 << i if c == '#' else 0 for i, c in enumerate(m.group(1))) for m in matches]
    button_toggles = [[sum(1 << int(x) for x in x_group.split(',')) for x_group in m.group(2).strip(" ()").split(') (')] for m in matches]
    joltage_requirements = [[int(x) for x in m.group(4).split(',')] for m in matches]

    # We want the minimum number of xored together button toggles such that the result is equal to the indicator pattern
    result = 0
    for indicator_pattern, button_toggle in zip(indicator_patterns, button_toggles):
        min_presses = 0
        for n in range(1, len(button_toggle)+1):
            for combination in itertools.combinations(button_toggle, n):
                if functools.reduce(operator.xor, combination, 0) == indicator_pattern:
                    min_presses = n
                    break
            if min_presses > 0:
                break
        result += min_presses

    return result


def day10_part2_algorithm(input_str: str) -> int:
    pass


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        data = f.read().strip()
    result = day10_part1_algorithm(data)

    return result


if __name__ == "__main__":
    print(main())
