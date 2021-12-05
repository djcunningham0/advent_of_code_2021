from shared import read_text_file
from collections import defaultdict
from typing import List


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        self.xrange = range(start.x, end.x + 1) if start.x <= end.x else range(start.x, end.x - 1, -1)
        self.yrange = range(start.y, end.y + 1) if start.y <= end.y else range(start.y, end.y - 1, -1)

    def get_points_on_line(self) -> List[Point]:
        xrange = self.xrange if len(self.xrange) > 1 else [self.xrange[0]] * len(self.yrange)
        yrange = self.yrange if len(self.yrange) > 1 else [self.yrange[0]] * len(self.xrange)
        return [Point(x, y) for x, y in zip(xrange, yrange)]

    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y

    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    def __repr__(self):
        return f"Line({self.start}, {self.end})"


class Grid:
    def __init__(self):
        self.point_counts = defaultdict(int)

    def mark_point(self, p: Point):
        self.point_counts[(p.x, p.y)] += 1

    def mark_line(self, line: Line):
        [self.mark_point(p) for p in line.get_points_on_line()]

    def count_marked_points(self, min_value: int = 1) -> int:
        return len([x for x in self.point_counts.values() if x >= min_value])


def parse_data(path: str) -> List[Line]:
    data = read_text_file(path, dtype=str)
    return [parse_line(x) for x in data]


def parse_line(text_line: str) -> Line:
    split_line = text_line.split(" -> ")
    start = [int(x) for x in split_line[0].split(",")]
    end = [int(x) for x in split_line[1].split(",")]
    return Line(Point(start[0], start[1]), Point(end[0], end[1]))


if __name__ == "__main__":
    data = parse_data("data/05.txt")

    ### Part 1
    grid = Grid()
    data_subset = [x for x in data if x.is_horizontal() or x.is_vertical()]
    for line in data_subset:
        grid.mark_line(line)
    print(f"solution 05a: {grid.count_marked_points(min_value=2)}")

    ### Part 2
    # same thing, but with data rather than data_subset
    grid = Grid()
    for line in data:
        grid.mark_line(line)
    print(f"solution 05b: {grid.count_marked_points(min_value=2)}")
