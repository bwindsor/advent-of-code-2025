"""
https://adventofcode.com/2025/day/6
"""
import pathlib
import os
from io import BufferedReader
import re

OPERATOR_MULTIPLY = 0
OPERATOR_ADD = 1


def get_line_len(f: BufferedReader):
    """Looks backwards from the end of a file for the first \n character and returns the length of the final line
    including the \n at the end of that line"""

    f.seek(0, os.SEEK_END)
    # File pointer is now at the end of the file
    # Now find the length of a line
    try:
        f.seek(-1024, os.SEEK_CUR)
        data = f.read(1024)
    except OSError:  # Tried to move before start of file
        f.seek(0, os.SEEK_SET)
        data = f.read()

    data = data.rstrip(b'\n')  # Remove newlines from the end of the file
    newline_pos = data.rfind(b'\n')
    if newline_pos >= 0:
        line_len = len(
            data) - newline_pos  # (-1 for correctnesss, +1 to include newline at end which we stripped, cancels out)
    else:
        line_len = len(data) + 1
        while True:
            cur_pos = f.tell()
            try:
                f.seek(-2048, os.SEEK_CUR)
                data = f.read(1024)
            except OSError:  # Tried to move before start of file
                f.seek(0, os.SEEK_SET)
                data = f.read(cur_pos)
            newline_pos = data.rfind(b'\n')
            if newline_pos >= 0:
                line_len += len(data) - newline_pos - 1
                break
            else:
                line_len += len(data)

    return line_len


def column_iterator(f: BufferedReader, start_pos: int, line_len: int):
    f.seek(start_pos, os.SEEK_SET)
    data = f.read(1024)  # May return less than 1024 bytes if we are at the end of the file
    offset = 0
    while len(data) > 0:
        end_idx = 0
        for match in re.finditer(br'[\+\*] +', data):
            yield match.start() + offset, match.end() - match.start(), OPERATOR_MULTIPLY if b'*' in match.group(0) else OPERATOR_ADD
            end_idx = match.end()
        new_data = f.read(1024)
        if len(new_data) == 0:
            break
        offset += end_idx
        data = data[end_idx:] + new_data


def day6_part1_algorithm(input_filename: str) -> int:
    with open(input_filename, 'rb') as f:
        line_len = get_line_len(f)

        f.seek(0, os.SEEK_END)
        file_len = f.tell()
        num_lines = file_len // line_len

        result = 0
        with open(input_filename, 'rb') as f_op:
            for i_col, col_width, operator in column_iterator(f_op, line_len * (num_lines - 1), line_len):
                part_result = 0 if operator == OPERATOR_ADD else 1
                for i_row in range(0, num_lines - 1):
                    f.seek(i_row * line_len + i_col, os.SEEK_SET)
                    data = int(f.read(col_width))
                    if operator == OPERATOR_ADD:
                        part_result += data
                    else:
                        part_result *= data
                result += part_result

    return result


def day6_part2_algorithm(input_filename: str) -> int:
    with open(input_filename, 'rb') as f:
        line_len = get_line_len(f)

        f.seek(0, os.SEEK_END)
        file_len = f.tell()
        num_lines = file_len // line_len

        result = 0
        with open(input_filename, 'rb') as f_op:
            for i_col, col_width, operator in column_iterator(f_op, line_len * (num_lines - 1), line_len):
                data = []
                for i_row in range(0, num_lines - 1):
                    f.seek(i_row * line_len + i_col, os.SEEK_SET)
                    data.append(f.read(col_width))

                part_result = 0 if operator == OPERATOR_ADD else 1
                for i_x in range(col_width):
                    n = ''
                    for i_row in range(0, num_lines - 1):
                        n += chr(data[i_row][i_x])
                    if len(n.strip()) > 0:
                        if operator == OPERATOR_ADD:
                            part_result += int(n)
                        else:
                            part_result *= int(n)

                result += part_result

    return result


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    result = day6_part2_algorithm(str(input_file))

    return result


if __name__ == "__main__":
    print(main())
