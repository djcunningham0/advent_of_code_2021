"""
Not the most elegant solution but it works. There are probably some possible linear
algebra shortcuts but I used a bit of brute force instead. Runs in about 3.5 seconds.
"""

from __future__ import annotations

from shared import read_text_file
from typing import List, Tuple
from itertools import combinations
import numpy as np
from numpy.linalg import matrix_power


R_x = np.array([
    [1, 0, 0],
    [0, 0, -1],
    [0, 1, 0],
])
R_y = np.array([
    [0, 0, 1],
    [0, 1, 0],
    [-1, 0, 0],
])
R_z = np.array([
    [0, -1, 0],
    [1, 0, 0],
    [0, 0, 1],
])

ROTATION_MATRICES = [
    # all distinct rotations in 3d space
    # (https://www.euclideanspace.com/maths/geometry/rotations/euler/examples/index.htm)
    np.identity(3),
    R_x,
    R_x.dot(R_x),
    R_x.dot(R_x).dot(R_x),
    R_y,
    R_y.dot(R_x),
    R_y.dot(R_x).dot(R_x),
    R_y.dot(R_x).dot(R_x).dot(R_x),
    R_y.dot(R_y).dot(R_y),
    R_y.dot(R_y).dot(R_y).dot(R_x),
    R_y.dot(R_y).dot(R_y).dot(R_x).dot(R_x),
    R_y.dot(R_y).dot(R_y).dot(R_x).dot(R_x).dot(R_x),
    R_z,
    R_z.dot(R_x),
    R_z.dot(R_x).dot(R_x),
    R_z.dot(R_x).dot(R_x).dot(R_x),
    R_z.dot(R_z),
    R_z.dot(R_z).dot(R_x),
    R_z.dot(R_z).dot(R_x).dot(R_x),
    R_z.dot(R_z).dot(R_x).dot(R_x).dot(R_x),
    R_z.dot(R_z).dot(R_z),
    R_z.dot(R_z).dot(R_z).dot(R_x),
    R_z.dot(R_z).dot(R_z).dot(R_x).dot(R_x),
    R_z.dot(R_z).dot(R_z).dot(R_x).dot(R_x).dot(R_x),
]


class Scanner:
    def __init__(self, beacon_data: List[Tuple[int, int, int]], id_: int):
        self.id = id_
        self.v = np.array([0, 0, 0])
        self.beacons: List[np.array] = []
        self.scanner_locations: List[np.array] = [np.array([0, 0, 0])]  # this scanner is at 0,0,0
        for b in beacon_data:
            self.add_beacon(np.array([b[0], b[1], b[2]]))

    def add_beacon(self, v: np.array):
        self.beacons.append(v)

    def all_beacon_to_beacon_distances(self) -> List[float]:
        vectors = [v2 - v1 for v1, v2 in self.beacon_pairs()]
        return [np.linalg.norm(v) for v in vectors]

    def beacon_pairs(self):
        return combinations(self.beacons, 2)

    def transform_beacons(self, M: np.array, b: np.array):
        """Apply rotation matrix M and translation vector b to all beacon vectors"""
        for i, v in enumerate(self.beacons):
            self.beacons[i] = M.dot(v) + b

    def merge(self, other: Scanner, location_vector: np.array):
        """Merge with another scanner, i.e., add all beacons from that scanner"""
        current_beacons = set(tuple(v) for v in self.beacons)
        for b in other.beacons:
            if tuple(b) not in current_beacons:
                self.add_beacon(b)
        self.scanner_locations.append(location_vector)

    def scanner_manhattan_distances(self):
        n = len(self.scanner_locations)
        distances = np.zeros((n, n))
        for i, j in combinations(range(n), 2):
            distances[i][j] = np.abs(self.scanner_locations[i] - self.scanner_locations[j]).sum()
        return distances

    def __len__(self):
        return len(self.beacons)

    def __repr__(self):
        return f"Scanner(id={self.id}, <{len(self.beacons)} beacons>)"


def align_scanners(scanner_list: List[Scanner]) -> Scanner:
    # note: making a lot of assumptions here, e.g., that all distances are unique -- it works for this problem
    s0 = scanner_list.pop(0)  # use the first one as our reference beacon
    while scanner_list:
        # calculate beacon-to-beacon distances for all scanners and select the one with the most overlap
        #   note: could probably speed this search up a bit... as the reference scanner's beacon list grows,
        #   it takes longer to calculate all distance overlaps. We could short circuit that search once
        #   enough overlaps are found
        distances_0 = s0.all_beacon_to_beacon_distances()
        distance_overlaps = [len(set(distances_0).intersection(set(x.all_beacon_to_beacon_distances()))) for x in scanner_list]
        which_scanner = int(np.argmax(distance_overlaps))
        s = scanner_list.pop(which_scanner)
        distances_1 = s.all_beacon_to_beacon_distances()

        # find the equivalent beacon-to-beacon vectors
        pairs_0 = list(s0.beacon_pairs())
        pairs_1 = list(s.beacon_pairs())
        vectors_0 = [v2 - v1 for v1, v2 in pairs_0]
        vectors_1 = [v2 - v1 for v1, v2 in pairs_1]
        equivalent_indices = [(i, distances_1.index(x)) for i, x in enumerate(distances_0) if x in distances_1]
        equivalent_pairs = [(pairs_0[i], pairs_1[j]) for i, j in equivalent_indices]
        equivalent_vectors = [(vectors_0[i], vectors_1[j]) for i, j in equivalent_indices]

        # there's probably a slick linear algebra way to figure out the rotation matrix
        # and translation vector, but here's a mostly brute force approach

        # first find the rotation matrix
        short_circuit_amount = 12
        for i, M in enumerate(ROTATION_MATRICES):
            correct = 0
            orientations = [0] * len(equivalent_vectors)
            for j, (v0, v1) in enumerate(equivalent_vectors):
                if np.all(M.dot(v1) == v0):
                    correct += 1
                    orientations[j] = 1
                elif np.all(M.dot(-v1) == v0):
                    correct += 1
                    orientations[j] = -1

                # assume 12 correct vectors is enough evidence that M is correct
                if correct == short_circuit_amount:
                    break

            if correct == short_circuit_amount:
                break

        # now find the translation vector
        # (probably overkill to verify on all pairs but it doesn't cost much in performance)
        b = None
        for k, (p0, p1) in enumerate(equivalent_pairs):
            if orientations[k] == 0:
                # we didn't identify this vector correctly, so we can't use it to find translation
                continue
            v00, v01 = p0
            v10, v11 = [M.dot(v) for v in p1[::orientations[k]]]

            if b is None:
                b = v00 - v10
                assert np.all(v11 + b == v01)
            else:
                assert np.all(v10 + b == v00)
                assert np.all(v11 + b == v01)

        # update all the points in the other scanner, then merge into the reference scanner
        s.transform_beacons(M, b)
        s0.merge(s, b)

    return s0


def parse_data(path: str) -> List[Scanner]:
    data: List[str] = read_text_file(path)
    scanner_list = []
    for x in data:
        if not x:
            continue
        elif x.startswith("--- scanner"):
            scanner_list.append([])
        else:
            point = x.split(",")
            point = tuple(int(y) for y in point)
            scanner_list[-1].append(point)
    return [Scanner(beacon_data=x, id_=i) for i, x in enumerate(scanner_list)]


if __name__ == "__main__":
    data = parse_data("data/19.txt")

    ### Part 1
    s = align_scanners(data)
    print(f"Solution 19a: {len(s)}")

    ### Part 2
    print(f"Solution 19b: {int(s.scanner_manhattan_distances().max())}")
