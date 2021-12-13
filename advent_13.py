from collections import namedtuple
from typing import Tuple, List, Set


Point = namedtuple("Point", ["x", "y"])
Fold = namedtuple("Fold", ["axis", "location"])


class Grid:
    def __init__(self, points: List[Point]):
        self.marked_points: Set[Point] = set()
        for p in points:
            self.mark_point(p)

    def mark_point(self, p: Point):
        self.marked_points.add(p)

    def fold(self, fold: Fold):
        """
        Fold over the specified axis at the specified location. Remove any points
        outside the fold line and mark their new locations.
        """
        current_points = self.marked_points.copy()
        for p in current_points:
            compare_location = p.x if fold.axis == "x" else p.y
            if compare_location > fold.location:
                self.marked_points.remove(p)
                new_x = p.x if fold.axis == "y" else fold.location - (p.x - fold.location)
                new_y = p.y if fold.axis == "x" else fold.location - (p.y - fold.location)
                self.mark_point(Point(x=new_x, y=new_y))

    def process_multiple_folds(self, folds: List[Fold]):
        for fold in folds:
            self.fold(fold)

    def print_marked_points(self, file_path: str = None):
        max_x = max(p.x for p in self.marked_points)
        max_y = max(p.y for p in self.marked_points)
        out = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        for p in self.marked_points:
            out[p.y][p.x] = "#"

        if file_path:
            with open(file_path, "w") as f:
                for line in out:
                    f.write("".join(line) + "\n")
        else:
            for line in out:
                print("".join(line))


def parse_data(path: str) -> Tuple[List[Point], List[Fold]]:
    points = []
    folds = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                pass
            elif line.startswith("fold"):
                line = line.split("fold along ")[1]
                axis, location = line.split("=")
                folds.append(Fold(axis=axis, location=int(location)))
            else:
                x, y = line.split(",")
                points.append(Point(x=int(x), y=int(y)))
    return points, folds


if __name__ == "__main__":
    points, folds = parse_data("data/13.txt")

    ### Part 1
    grid = Grid(points)
    grid.fold(folds[0])
    print(f"Solution 13a: {len(grid.marked_points)}")

    ### Part 2
    grid.process_multiple_folds(folds[1:])
    grid.print_marked_points("data/13.out")  # view this file to get the code
