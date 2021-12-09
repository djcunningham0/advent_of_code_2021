from collections import defaultdict
from typing import List, Tuple, Optional


class LowPointMap:
    def __init__(self, data: List[List[int]]):
        """
        self.map: keys are (i, j) tuples representing points, values are (i, j, value)
        tuples representing location and value of the low point that the key leads to

        self.basins: keys are (i, j, value) tuples representing low points (there is
        one entry per low point), values are set of (i, j) points that lead to the key
        low point

        self.basins is basically an index for self.map
        """
        self.data = data
        self.n_rows = len(data)
        self.n_cols = len(data[0])

        self.map = dict()
        self.basins = defaultdict(set)

        self.find_low_points()

    def find_low_points(self):
        """Loop through the data and find the low point each point leads to."""
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                self.trace_to_low_point(i, j)

    def trace_to_low_point(self, i, j, _history: List = None):
        """
        Start from a given point and trace all the way to the low point it leads to.
        Record the path history once we find the low point.
        """
        if self.data[i][j] == 9:
            return None  # 9 never belongs to a basin
        _history = _history or []
        _history.append((i, j))
        next_point = self.find_lowest_neighbor(i, j)
        if next_point is None:
            low_point = (i, j, self.data[i][j])
            self.record_history(_history, low_point)
        elif next_point in self.map:
            low_point = self.map[next_point]
            self.record_history(_history, low_point)
        else:
            self.trace_to_low_point(next_point[0], next_point[1], _history)

    def find_lowest_neighbor(self, i: int, j: int) -> Optional[Tuple[int, int]]:
        """Return the coordinates of the lowest neighboring point"""
        up = self.data[i - 1][j] if i > 0 else 9
        down = self.data[i + 1][j] if i < self.n_rows - 1 else 9
        left = self.data[i][j - 1] if j > 0 else 9
        right = self.data[i][j + 1] if j < self.n_cols - 1 else 9
        min_val = min(up, down, left, right)
        if min_val == 9 or min_val > self.data[i][j]:
            return None  # if we're at a low point, don't move anywhere
        else:
            locations = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
            return locations[[up, down, left, right].index(min_val)]

    def record_history(self, history: List[Tuple[int, int]], low_point: Tuple[int, int, int]):
        """
        Record the information we learned about a low point.

        :param history: a list of (i, j) points representing the path that was followed
        to reach the low point
        :param low_point: (i, j, value) tuple for the low point
        """
        for x in history:
            self.map[x] = low_point
            self.basins[low_point].add(x)

    def score_low_points(self) -> int:
        low_points = list(set(self.map.values()))
        return sum(x[2] + 1 for x in low_points)

    def find_largest_basins(self, n: int = 3):
        basin_sizes = [len(val) for k, val in self.basins.items()]
        return sorted(basin_sizes, reverse=True)[:n]


def parse_data(path: str):
    data = []
    with open(path, "r") as f:
        for line in f:
            data.append([int(x) for x in line.strip()])
    return data


if __name__ == "__main__":
    data = parse_data("data/09.txt")
    low_point_map = LowPointMap(data)

    ### Part 1
    score = low_point_map.score_low_points()
    print(f"Solution 09a: {score}")

    ### Part 2
    largest_basins = low_point_map.find_largest_basins()
    print(f"Solution 09b: {largest_basins[0] * largest_basins[1] * largest_basins[2]}")
