"""
https://adventofcode.com/2025/day/9
"""
import pathlib

from numba.core.ir import Raise


def day9_part1_algorithm(input_str: str) -> int:
    """
    Maximise over i, j
    (y_i - y_j + 1) * (x_i - x_j + 1)

    The distance metric between tiles i, j is (y_i - y_j) * (x_i - x_j)
    and we want to find the pair of tiles which are furthest apart using this metric

    This just checks all pairs of tiles...probably not the most efficient algorithm
    """

    red_tile_locations = [[int(x) for x in line.split(',')] for line in input_str.split('\n')]
    max_d = 0
    for i in range(len(red_tile_locations)):
        for j in range(i+1, len(red_tile_locations)):
            d = abs(red_tile_locations[i][0] - red_tile_locations[j][0] + 1) * abs(red_tile_locations[i][1] - red_tile_locations[j][1] + 1)
            if d > max_d:
                max_d = d
    return max_d


def day9_part2_algorithm(input_str: str) -> int:
    """
    Maximise over i, j
    (y_i - y_j + 1) * (x_i - x_j + 1)
    with constraints
    1. (x_i, y_j) must be green or red (inside or on border of shape)
    2. (x_j, y_i) must be green or red (inside or on border of shape)
    3. The four vectors forming the edges of the rectangle must not intersect leave the shape

    We can check if a point is inside the shape by taking a vector from (0, y_i) to (x_i, y_i) and seeing how many
    edges this intersects. If the number of edges is odd, it is inside the shape.
    """

    red_tile_locations = [[int(x) for x in line.split(',')] for line in input_str.split('\n')]
    N = len(red_tile_locations)
    edge_vectors = [[red_tile_locations[(i+1) % N][0]-red_tile_locations[i][0], red_tile_locations[(i+1) % N][1]-red_tile_locations[i][1]] for i in range(N)]
    edge_vectors_with_start = [(p, v) for p, v in zip(red_tile_locations, edge_vectors)]
    vertical_edge_vectors = [(t, v[1]) for t, v in zip(red_tile_locations, edge_vectors) if v[0] == 0]

    # Get list of edge tile locations
    edge_tile_locations = get_edge_tile_locations(red_tile_locations)

    max_d = 0
    for i in range(len(red_tile_locations)):
        for j in range(i+1, len(red_tile_locations)):
            d = abs(red_tile_locations[i][0] - red_tile_locations[j][0] + 1) * abs(red_tile_locations[i][1] - red_tile_locations[j][1] + 1)
            if d > max_d:
                if is_inside(edge_tile_locations, vertical_edge_vectors, (red_tile_locations[i][0], red_tile_locations[j][1])) and \
                    is_inside(edge_tile_locations, vertical_edge_vectors, (red_tile_locations[j][0], red_tile_locations[i][1])) and \
                    is_vector_inside(edge_vectors_with_start, (red_tile_locations[i][0], red_tile_locations[i][1]), (red_tile_locations[i][0], red_tile_locations[j][1])) and \
                    is_vector_inside(edge_vectors_with_start, (red_tile_locations[i][0], red_tile_locations[j][1]), (red_tile_locations[j][0], red_tile_locations[j][1])) and \
                    is_vector_inside(edge_vectors_with_start, (red_tile_locations[j][0], red_tile_locations[j][1]), (red_tile_locations[j][0], red_tile_locations[i][1])) and \
                    is_vector_inside(edge_vectors_with_start, (red_tile_locations[j][0], red_tile_locations[i][1]), (red_tile_locations[i][0], red_tile_locations[i][1])):
                    max_d = d
    return max_d


def get_edge_tile_locations(red_tile_locations: list[list[int]]):
    edge_tile_locations = set()
    for i, red_tile in enumerate(red_tile_locations):
        next_idx = (i+1) % len(red_tile_locations)
        next_tile = red_tile_locations[next_idx]
        if red_tile[0] == next_tile[0]:
            for y in range(min(red_tile[1], next_tile[1]), max(red_tile[1], next_tile[1])+1):
                edge_tile_locations.add((red_tile[0], y))
        elif red_tile[1] == next_tile[1]:
            for x in range(min(red_tile[0], next_tile[0]), max(red_tile[0], next_tile[0])+1):
                edge_tile_locations.add((x, red_tile[1]))
        else:
            raise Exception("Expected next tile to be horizontal or vertical")
    return edge_tile_locations


def is_vector_inside(edge_vectors: list[tuple[list[int],list[int]]], p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    if p1[0] == p2[0]:
        # Case where vector is vertical, so compare to horizontal edges
        horizontal_edge_vectors = filter(lambda v: v[1][1] == 0, edge_vectors)
        intersecting_vector_candidates = list(filter(lambda v: (
            ((v[0][0] <= p1[0] <= v[0][0] + v[1][0]) or (v[0][0] >= p1[0] >= v[0][0] + v[1][0]))
            and
            (p1[1] < v[0][1] < p2[1] or p2[1] < v[0][1] < p1[1])
        ), horizontal_edge_vectors))
        if len(intersecting_vector_candidates) == 0:
            return True
        max_x = max(map(lambda v: max(v[0][0], v[0][0] + v[1][0]), intersecting_vector_candidates))
        min_x = min(map(lambda v: min(v[0][0], v[0][0] + v[1][0]), intersecting_vector_candidates))
        if max_x <= p1[0] or min_x >= p1[0]:
            return True
        else:
            return False
    elif p1[1] == p2[1]:
        # Case where vector is horizontal
        vertical_edge_vectors = filter(lambda v: v[1][0] == 0, edge_vectors)
        intersecting_vector_candidates = list(filter(lambda v: (
            ((v[0][1] <= p1[1] <= v[0][1] + v[1][1]) or (v[0][1] >= p1[1] >= v[0][1] + v[1][1]))
            and
            (p1[0] < v[0][0] < p2[0] or p2[0] < v[0][0] < p1[0])
        ), vertical_edge_vectors))
        if len(intersecting_vector_candidates) == 0:
            return True

        max_y = max(map(lambda v: max(v[0][1], v[0][1] + v[1][1]), intersecting_vector_candidates))
        min_y = min(map(lambda v: min(v[0][1], v[0][1] + v[1][1]), intersecting_vector_candidates))
        if max_y <= p1[1] or min_y >= p1[1]:
            return True
        else:
            return False
    else:
        raise Exception("Unhandled case")


def is_inside(edge_tile_locations: set[tuple[int, int]], vertical_edge_vectors: list[tuple[list[int], int]], point: tuple[int, int]) -> bool:
    if point in edge_tile_locations:
        return True

    # Now point is fully inside or fully outside the shape
    vertical_edge_vectors_left_of_point = filter(lambda x: x[0][0] < point[0], vertical_edge_vectors)
    vertical_edge_vectors_intersecting = filter(lambda x: (
            (x[0][1] <= point[1] < x[0][1] + x[1]) or (x[0][1] > point[1] >= x[0][1] + x[1])
    ), vertical_edge_vectors_left_of_point)
    num_intersects = len(list(vertical_edge_vectors_intersecting))

    return (num_intersects % 2) != 0

def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        data = f.read().strip()
    result = day9_part2_algorithm(data)

    return result


if __name__ == "__main__":
    print(main())
