"""
https://adventofcode.com/2025/day/10
"""
import pathlib
import re
import itertools
import functools
import operator
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint


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
    """

    Given buttons 0-n, let ai be the number of times button i is pressed
    Then for this example:
    (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}

    a4 + a5 = 3
    a1 + a5 = 5
    a2 + a3 + a4 = 4
    a0 + a1 + a3 = 7
    a_i >= 0 for all i

    Or in matrix form:
    [0 0 0 0 1 1][a0] = [3]
    [0 1 0 0 0 1][a1] = [5]
    [0 0 1 1 1 0][a2] = [4]
    [1 1 0 1 0 0][a3] = [7]
                 [a4]
                 [a5]

    Minimise sum(ai) subject to these constraints.

    This can be solved with the simplex algorithm.
    Would be nice to implement this myself but it will take to long...so I'll use scipy!
    """

    lines = input_str.split('\n')
    matches = [re.match(r"\[([.#]+)] ((\([,\d]+\) )+)\{([,\d]+)\}", line) for line in lines]
    button_toggles = [[[int(x) for x in x_group.split(',')] for x_group in m.group(2).strip(" ()").split(') (')]
                      for m in matches]
    joltage_requirements = [[int(x) for x in m.group(4).split(',')] for m in matches]

    result = 0
    for button_toggle, joltage_requirement in zip(button_toggles, joltage_requirements):
        A = np.zeros((len(joltage_requirement), len(button_toggle)), dtype=int)
        for i, t in enumerate(button_toggle):
            for x in t:
                A[x, i] = 1

        b = np.array(joltage_requirement)

        # Constraint is Ax = b where x is vector of how many times each button is pressed
        # Optimisation problem is to minimise a0 + a1 + ... + an

        opt_result = milp(
            c=np.ones(len(button_toggle)),
            constraints=LinearConstraint(A, lb=b, ub=b),
            bounds=Bounds(0, np.inf),
            integrality=np.ones(len(button_toggle), dtype=int), # This enforces integer only solutions
        )

        result += int(sum(opt_result.x))

    return result


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        data = f.read().strip()
    result = day10_part2_algorithm(data)

    return result


if __name__ == "__main__":
    print(main())
