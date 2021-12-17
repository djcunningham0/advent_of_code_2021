"""
Use Dijkstra's algorithm with a priority queue to find the shortest path between points.
Runs in less than a second for a 500x500 grid.
https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
"""

from shared import read_text_file
from collections import defaultdict
from functools import reduce
from math import inf
import heapq

from typing import List, Tuple, Dict, Union


def parse_data(path: str) -> List[List[int]]:
    data = read_text_file(path)
    return [[int(x) for x in line] for line in data]


def expand_data(data: List[List[int]], n: int = 5) -> List[List[int]]:
    """Expand the data into a larger grid as described in the prompt."""
    new_data = []
    n_cols = len(data[0])
    for i in range(n):
        for line in data:
            add_vals = reduce(lambda a, b: a + b, [[x] * n_cols for x in range(n)])
            add_vals = [x + i for x in add_vals]
            new_line = [x + y for x, y in zip(line * n, add_vals)]
            new_line = [x if x <= 9 else x % 9 for x in new_line]
            new_data.append(new_line)
    return new_data


class Grid:
    def __init__(self, data: List[List[int]]):
        self.data = data
        self.n_rows = len(data)
        self.n_cols = len(data[0])
        assert all(len(x) == self.n_cols for x in data)

        self.start = (0, 0)
        self.destination = (self.n_rows - 1, self.n_cols - 1)

        self.distances: Dict[Tuple[int, int], Union[int, float]] = defaultdict(lambda: inf)
        self.distances[(self.start[0], self.start[1])] = 0

    def get_neighbors(self, i: int, j: int) -> List[Tuple[int, int]]:
        neighbors = []
        if i < self.n_cols - 1:
            neighbors.append((i+1, j))
        if j < self.n_rows - 1:
            neighbors.append((i, j+1))
        if i > 0:
            neighbors.append((i-1, j))
        if j > 0:
            neighbors.append((i, j-1))
        return neighbors

    def dijkstra(self, early_stopping: bool = True):
        # set up a priority queue that will be sorted by distance
        heap: List[Tuple[int, Tuple[int, int]]] = []
        heapq.heappush(heap, (0, self.start))  # (distance, (i, j))

        # keep track of visited points and known distances to all points
        visited = set()

        while heap:
            # take the first point in the queue, which will be the one with the shortest distance to it
            _, current_node = heapq.heappop(heap)
            if current_node in visited:
                continue
            visited.add(current_node)
            distance = self.distances[current_node]

            # if we've reached the destination, we're done
            if current_node == self.destination and early_stopping:
                return distance

            # get the distance to each neighbor -- if it's less than we've seen previously, add it to the queue
            i, j = current_node
            for next_i, next_j in self.get_neighbors(i, j):
                if (next_i, next_j) in visited:
                    continue
                new_distance = distance + self.data[next_i][next_j]
                if new_distance < self.distances[(next_i, next_j)]:
                    self.distances[(next_i, next_j)] = new_distance
                    heapq.heappush(heap, (new_distance, (next_i, next_j)))

        return self.distances[self.destination]


if __name__ == "__main__":
    data = parse_data("data/15.txt")

    ### Part 1
    grid = Grid(data)
    solution = grid.dijkstra()
    print(f"Solution 15a: {solution}")

    ### Part 2
    expanded_data = expand_data(data)
    expanded_grid = Grid(expanded_data)
    solution = expanded_grid.dijkstra()
    print(f"Solution 15b: {solution}")
