import pytest
from day8.day8 import day8_part1_algorithm, day8_part2_algorithm, KDTree, Point, Bounds, XYZ


def test_kdtree_nearest_point():
    points = [
        Point(100, 0, 0, 0),
        Point(101, 0, 10, 0),
        Point(102, 0, 0, 10),
        Point(103, 10, 0, 10),
        Point(104, 0, 10, 10),
        Point(105, 10, 10, 10),
    ]
    tree = KDTree(points)
    assert tree.nearest_point(Point(0, 0, 0, 0), set()) == (0, points[0])
    assert tree.nearest_point(Point(100, 0, 0, 0), {100}) == (10**2, points[2])
    assert tree.nearest_point(Point(0, 10, 0, 10), set()) == (0, points[3])
    assert tree.nearest_point(Point(0, 10, 11, 10), set()) == (1, points[5])


def test_kdtree_construct():
    points = [
        Point(0, 10, 200, 1),
        Point(0, 20, 400, 5),
        Point(0, 30, 500, 1),

        Point(0, 40, 100, 1),

        Point(0, 50, 200, 2),
        Point(0, 60, 300, 1),
    ]
    tree = KDTree(points)
    assert tree.root_node.p is points[3]
    assert tree.root_node.bounds == Bounds(XYZ(0, 0, 0), XYZ(60, 500, 5))

    assert tree.root_node.left_child.p is points[1]
    assert tree.root_node.right_child.p is points[5]
    assert tree.root_node.left_child.bounds == Bounds(XYZ(0, 0, 0), XYZ(40, 500, 5))
    assert tree.root_node.right_child.bounds == Bounds(XYZ(40, 0, 0), XYZ(60, 500, 5))

    assert tree.root_node.left_child.left_child.p is points[0]
    assert tree.root_node.left_child.right_child.p is points[2]
    assert tree.root_node.right_child.left_child.p is points[4]
    assert tree.root_node.right_child.right_child is None

    assert tree.root_node.left_child.left_child.left_child is None
    assert tree.root_node.left_child.left_child.right_child is None
    assert tree.root_node.left_child.right_child.left_child is None
    assert tree.root_node.left_child.right_child.right_child is None
    assert tree.root_node.right_child.left_child.left_child is None
    assert tree.root_node.right_child.left_child.right_child is None


def test_day8_part1_full():
    test_input = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689""".replace("\r", "")
    expected_output = 40
    assert day8_part1_algorithm(test_input, 10) == expected_output


def test_day8_part2_full():
    test_input = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689""".replace("\r", "")
    expected_output = 25272
    assert day8_part2_algorithm(test_input) == expected_output
