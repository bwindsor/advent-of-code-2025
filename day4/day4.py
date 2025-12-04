"""
https://adventofcode.com/2025/day/4
"""
import pathlib


def day4_part1_algorithm(rolls_map: str) -> int:
    """
    Convert the map into a binary image 0 = no roll, 1 = roll
    Convolve with kernel
    [1 1 1
     1 0 1
     1 1 1]
    Element-wise multiply with inverse of original image, to only include pixels where there is a roll
    Find how many convolved pixels are < 4

    Could use image processing libraries to process convolution more efficiently with FFT methods, but since our input
    isn't that large just use the brute force convolution
    """
    m = [([0] + [1 if c == "@" else 0 for c in x.strip()] + [0]) for x in rolls_map.split('\n')]
    m.insert(0, [0] * len(m[0]))
    m.append([0] * len(m[0]))
    k = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]

    result = 0
    for i_y in range(1, len(m)-1):
        for i_x in range(1, len(m[0]) - 1):
            if m[i_y][i_x] == 1:
                total = m[i_y+1][i_x] + m[i_y-1][i_x] + m[i_y][i_x+1] + m[i_y][i_x-1] + m[i_y+1][i_x+1] + m[i_y-1][i_x-1] + m[i_y+1][i_x-1] + m[i_y-1][i_x+1]
                if total < 4:
                    result += 1
    return result


def day4_part2_algorithm(rolls_map: str) -> int:
    m = [([0] + [1 if c == "@" else 0 for c in x.strip()] + [0]) for x in rolls_map.split('\n')]
    m.insert(0, [0] * len(m[0]))
    m.append([0] * len(m[0]))
    m2 = [x.copy() for x in m]
    k = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]

    result = 0

    while True:
        result_this_step = 0
        for i_y in range(1, len(m) - 1):
            for i_x in range(1, len(m[0]) - 1):
                if m[i_y][i_x] == 1:
                    total = m[i_y + 1][i_x] + m[i_y - 1][i_x] + m[i_y][i_x + 1] + m[i_y][i_x - 1] + m[i_y + 1][i_x + 1] + \
                            m[i_y - 1][i_x - 1] + m[i_y + 1][i_x - 1] + m[i_y - 1][i_x + 1]
                    if total < 4:
                        result_this_step += 1
                        # Remove roll
                        m2[i_y][i_x] = 0

        if result_this_step == 0:
            break

        result += result_this_step
        # Swap
        tmp = m
        m = m2
        m2 = m

    return result


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        data = f.read()
    result = day4_part2_algorithm(data)

    return result


if __name__ == "__main__":
    print(main())
