"""
https://adventofcode.com/2025/day/8
"""
import pathlib
from typing import NamedTuple, Optional


class XYZ(NamedTuple):
    x: int
    y: int
    z: int

    def rotate(self) -> 'XYZ':
        return XYZ(self.y, self.z, self.x)

    def distance2_to(self, other: 'XYZ') -> int:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2


class Bounds(NamedTuple):
    minimum: XYZ
    maximum: XYZ

    def rotate(self) -> 'Bounds':
        return Bounds(self.minimum.rotate(), self.maximum.rotate())

    def diagonal2(self) -> int:
        return (self.maximum.x - self.minimum.x)**2 + (self.maximum.y - self.minimum.y)**2 + (self.maximum.z - self.minimum.z)**2

class Point(NamedTuple):
    idx: int
    x: int
    y: int
    z: int

    def distance2_to(self, other: 'Point') -> int:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2

    def xyz(self) -> XYZ:
        return XYZ(self.x, self.y, self.z)


class Node:
    def __init__(self, p: Point, parent: Optional['Node'], left_child: Optional['Node'], right_child: Optional['Node'], left_children: list['Point'], right_children: list['Point'], bounds: Bounds):
        self.p = p
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child
        self.left_children = left_children
        self.right_children = right_children
        self.bounds = bounds

    def build_children(self, dimension: int) -> bool:
        # Returns True if this is a leaf node. Recursively builds children
        if dimension == 0:
            left_points = sorted(self.left_children, key=lambda p: p.x)
            right_points = sorted(self.right_children, key=lambda p: p.x)
            left_bounds = Bounds(XYZ(self.bounds.minimum.x, self.bounds.minimum.y, self.bounds.minimum.z),
                                 XYZ(self.bounds.maximum.x, self.bounds.maximum.y, self.p.z))
            right_bounds = Bounds(XYZ(self.bounds.minimum.x, self.bounds.minimum.y, self.p.z),
                                  XYZ(self.bounds.maximum.x, self.bounds.maximum.y, self.bounds.maximum.z))

        elif dimension == 1:
            left_points = sorted(self.left_children, key=lambda p: p.y)
            right_points = sorted(self.right_children, key=lambda p: p.y)
            left_bounds = Bounds(XYZ(self.bounds.minimum.x, self.bounds.minimum.y, self.bounds.minimum.z),
                                 XYZ(self.p.x, self.bounds.maximum.y, self.bounds.maximum.z))
            right_bounds = Bounds(XYZ(self.p.x, self.bounds.minimum.y, self.bounds.minimum.z),
                                  XYZ(self.bounds.maximum.x, self.bounds.maximum.y, self.bounds.maximum.z))

        else:
            left_points = sorted(self.left_children, key=lambda p: p.z)
            right_points = sorted(self.right_children, key=lambda p: p.z)
            left_bounds = Bounds(XYZ(self.bounds.minimum.x, self.bounds.minimum.y, self.bounds.minimum.z),
                                 XYZ(self.bounds.maximum.x, self.p.y, self.bounds.maximum.z))
            right_bounds = Bounds(XYZ(self.bounds.minimum.x, self.p.y, self.bounds.minimum.z),
                                  XYZ(self.bounds.maximum.x, self.bounds.maximum.y, self.bounds.maximum.z))

        if len(left_points) > 0:
            middle_point_left = left_points[len(left_points) // 2]
            self.left_child = Node(middle_point_left, self, None, None, left_points[:len(left_points) // 2], left_points[len(left_points) // 2 + 1:], left_bounds)
            self.left_child.build_children((dimension+1) % 3)

        if len(right_points) > 0:
            middle_point_right = right_points[len(right_points) // 2]
            self.right_child = Node(middle_point_right, self, None, None, right_points[:len(right_points) // 2], right_points[len(right_points) // 2 + 1:], right_bounds)
            self.right_child.build_children((dimension+1) % 3)

        return len(left_points) == 0 and len(right_points) == 0


class KDTree:
    def __init__(self, points: list[Point]) -> None:
        self.points = points
        n = len(points)
        points_sorted_x = sorted(points, key=lambda p: p.x)
        root_node = Node(points_sorted_x[n // 2], None, None, None, points_sorted_x[:n // 2], points_sorted_x[n // 2 + 1:],
                         Bounds(XYZ(0, 0, 0), XYZ(max(map(lambda p: p.x, points)), max(map(lambda p: p.y, points)), max(map(lambda p: p.z, points)))))
        root_node.build_children(1)
        self.root_node = root_node

    def _check_edge(self, p: XYZ, bounds: Bounds):
        if bounds.minimum.x <= p.x <= bounds.maximum.x:
            if p.y < bounds.minimum.y and p.z < bounds.minimum.z:
                return (p.y - bounds.minimum.y) ** 2 + (p.z - bounds.minimum.z) ** 2
            elif p.y < bounds.minimum.y and p.z > bounds.maximum.z:
                return (p.y - bounds.minimum.y) ** 2 + (p.z - bounds.maximum.z) ** 2
            elif p.y > bounds.maximum.y and p.z < bounds.minimum.z:
                return (p.y - bounds.maximum.y) ** 2 + (p.z - bounds.minimum.z) ** 2
            elif p.y > bounds.maximum.y and p.z > bounds.maximum.z:
                return (p.y - bounds.maximum.y) ** 2 + (p.z - bounds.maximum.z) ** 2
        return None

    def _check_face(self, p: XYZ, bounds: Bounds):
        if bounds.minimum.x <= p.x <= bounds.maximum.x and bounds.minimum.y <= p.y <= bounds.maximum.y and p.z > bounds.maximum.z:
            return (p.z - bounds.maximum.z)**2
        if bounds.minimum.x <= p.x <= bounds.maximum.x and bounds.minimum.y <= p.y <= bounds.maximum.y and p.z < bounds.minimum.z:
            return (bounds.minimum.z - p.z)**2
        return None

    def nearest_bbox_point2(self, point: XYZ, bounds: Bounds):
        # Case inside box
        if bounds.minimum.x <= point.x <= bounds.maximum.x and bounds.minimum.y <= point.y <= bounds.maximum.y and bounds.minimum.z <= point.z <= bounds.maximum.z:
            return 0

        # Case nearest point is a face
        d = self._check_face(point, bounds)
        if d is not None:
            return d
        d = self._check_face(point.rotate(), bounds.rotate())
        if d is not None:
            return d
        d = self._check_face(point.rotate().rotate(), bounds.rotate().rotate())
        if d is not None:
            return d

        # Case point is nearest an edge
        d = self._check_edge(point, bounds)
        if d is not None:
            return d
        d = self._check_edge(point.rotate(), bounds.rotate())
        if d is not None:
            return d
        d = self._check_edge(point.rotate().rotate(), bounds.rotate().rotate())
        if d is not None:
            return d

        # Case point is nearest a vertex
        if point.x < bounds.minimum.x and point.y < bounds.minimum.y and point.z < bounds.minimum.z:
            return point.distance2_to(XYZ(bounds.minimum.x, bounds.minimum.y, bounds.minimum.z))
        if point.x < bounds.minimum.x and point.y < bounds.minimum.y and point.z > bounds.maximum.z:
            return point.distance2_to(XYZ(bounds.minimum.x, bounds.minimum.y, bounds.maximum.z))
        if point.x < bounds.minimum.x and point.y > bounds.maximum.y and point.z < bounds.minimum.z:
            return point.distance2_to(XYZ(bounds.minimum.x, bounds.maximum.y, bounds.minimum.z))
        if point.x < bounds.minimum.x and point.y > bounds.maximum.y and point.z > bounds.maximum.z:
            return point.distance2_to(XYZ(bounds.minimum.x, bounds.maximum.y, bounds.maximum.z))
        if point.x > bounds.maximum.x and point.y < bounds.minimum.y and point.z < bounds.minimum.z:
            return point.distance2_to(XYZ(bounds.maximum.x, bounds.minimum.y, bounds.minimum.z))
        if point.x > bounds.maximum.x and point.y < bounds.minimum.y and point.z > bounds.maximum.z:
            return point.distance2_to(XYZ(bounds.maximum.x, bounds.minimum.y, bounds.maximum.z))
        if point.x > bounds.maximum.x and point.y > bounds.maximum.y and point.z < bounds.minimum.z:
            return point.distance2_to(XYZ(bounds.maximum.x, bounds.maximum.y, bounds.minimum.z))
        if point.x > bounds.maximum.x and point.y > bounds.maximum.y and point.z > bounds.maximum.z:
            return point.distance2_to(XYZ(bounds.maximum.x, bounds.maximum.y, bounds.maximum.z))

        raise Exception("No nearest point found")

    def nearest_point(self, point: Point) -> tuple[int, Point]:
        best_distance, best_node = self._nearest_point(point, self.root_node, self.root_node.bounds.diagonal2(), self.root_node)
        return best_distance, best_node.p

    def _nearest_point(self, point: Point, node: Node, best_distance: int, best_node: Node) -> tuple[int, Node]:
        # Traverse the tree and ignore any branches whose bounding box is further than the best distance found so far
        if node.p.idx != point.idx:
            possible_distance = point.distance2_to(node.p)
            if possible_distance < best_distance:
                best_distance = possible_distance
                best_node = node

        # Left
        if node.left_child is not None:
            nearest_point_of_bbox = self.nearest_bbox_point2(point.xyz(), node.left_child.bounds)
            if nearest_point_of_bbox < best_distance:
                # Consider this node
                possible_distance, possible_node = self._nearest_point(point, node.left_child, best_distance, best_node)
                if possible_distance < best_distance:
                    best_distance = possible_distance
                    best_node = possible_node

        # Right
        if node.right_child is not None:
            nearest_point_of_bbox = self.nearest_bbox_point2(point.xyz(), node.right_child.bounds)
            if nearest_point_of_bbox < best_distance:
                # Consider this node
                possible_distance, possible_node = self._nearest_point(point, node.right_child, best_distance, best_node)
                if possible_distance < best_distance:
                    best_distance = possible_distance
                    best_node = possible_node

        return best_distance, best_node


def day8_part1_algorithm(input_str: str) -> int:
    data = [Point(i, u[0], u[1], u[2]) for i, u in enumerate([[int(x) for x in line.split(',')] for line in input_str.split('\n')])]
    tree = KDTree(data)
    circuits = []
    wires_used = 0

    while wires_used < 10:
        best_distance2 = tree.root_node.bounds.diagonal2()
        p1 = None
        p2 = None
        for p in data:
            nearest_point2, nearest_point = tree.nearest_point(p)
            if nearest_point2 < best_distance2:
                best_distance2 = nearest_point2
                p1 = p
                p2 = nearest_point

        # Now we want to join p1 and p2
        p1_idx = -1
        p2_idx = -1
        for i, s in enumerate(circuits):
            if p1.idx in s:
                p1_idx = i
            if p2.idx in s:
                p2_idx = i

        if p1_idx == p2_idx and p1_idx >= 0 and p2_idx >= 0:
            # Already in the same circuit, do nothing
            pass
        elif p1_idx >= 0 and p2_idx < 0:
            # Add p2 to p1's set
            circuits[p1_idx].add(p2.idx)
            wires_used += 1
        elif p2_idx >= 0 and p1_idx < 0:
            # Add p1 to p2's set
            circuits[p2_idx].add(p1.idx)
            wires_used += 1
        elif p1_idx < 0 and p2_idx < 0:
            # New circuit
            circuits.append({p1.idx, p2.idx})
            wires_used += 1

    circuit_sizes = sorted([len(s) for s in circuits])
    return circuit_sizes[-1] * circuit_sizes[-2] * circuit_sizes[-3]


def day8_part2_algorithm(input_str: str) -> int:
    pass


def main():
    this_folder = pathlib.Path(__file__)
    input_file = this_folder.parent / 'input.txt'

    with open(input_file, 'r') as f:
        data = f.read().strip()
    result = day8_part1_algorithm(data)

    return result


if __name__ == "__main__":
    print(main())
