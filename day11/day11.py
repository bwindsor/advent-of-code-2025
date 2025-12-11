"""
https://adventofcode.com/2025/day/11
"""
import pathlib


def day11_part1_algorithm(input_str: str) -> int:
    lines = input_str.split('\n')
    graph = dict()
    parts = [line.split(': ') for line in lines]
    for part in parts:
        x = set()
        for s in part[1].split(' '):
            x.add(s)
        graph[part[0]] = x

    count = {"you": 1}

    result = 0
    while True:
        count_part = dict()
        for k, v in count.items():
            next_targets = graph[k]
            for n in next_targets:
                if n in count_part:
                    count_part[n] += v
                else:
                    count_part[n] = v
        count = count_part
        result += count.pop("out", 0)
        if len(count) == 0:
            break

    return result


def day11_part2_algorithm(input_str: str) -> int:
    lines = input_str.split('\n')
    graph = dict()
    parts = [line.split(': ') for line in lines]
    for part in parts:
        x = set()
        for s in part[1].split(' '):
            x.add(s)
        graph[part[0]] = x

    count = {"svr": (1, 0, 0, 0)}  # Format is (count, count_visited_dac, count_visited_fft, count_visited_both)

    result = 0
    while True:
        count_part = dict()
        for k, v in count.items():
            next_targets = graph[k]
            for n in next_targets:
                if n in count_part:
                    count_part[n] = (
                        count_part[n][0] + v[0],
                        count_part[n][1] + (v[0] if k == "dac" else v[1]),
                        count_part[n][2] + (v[0] if k == "fft" else v[2]),
                        count_part[n][3] + (v[1] if k == "fft" else (v[2] if k == "dac" else v[3]))
                    )
                else:
                    count_part[n] = (
                        v[0],
                        v[0] if k == "dac" else v[1],
                        v[0] if k == "fft" else v[2],
                        v[1] if k == "fft" else (v[2] if k == "dac" else v[3]),
                    )
        count = count_part
        result += count.pop("out", (0, 0, 0, 0))[3]
        if len(count) == 0:
            break

    return result


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        data = f.read().strip()
    result = day11_part2_algorithm(data)

    return result


if __name__ == "__main__":
    print(main())
