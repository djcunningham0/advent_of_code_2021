from shared import read_text_file
from typing import List


class Grid:
    def __init__(self, data: List[List[str]]):
        self.data = data
        self.n_rows = len(data)
        self.n_cols = len(data[0])
        assert all(len(x) == len(data[0]) for x in data)

    def move(self) -> bool:
        return self._do_move("east") | self._do_move("south")  # "|" instead of "or" to avoid short circuiting

    def _do_move(self, direction: str) -> bool:
        data = self.data if direction == "east" else transpose(self.data)
        arrow = ">" if direction == "east" else "v"
        new_data = []
        changed = False
        for row in data:
            can_move = [x == arrow and row[(i + 1) % len(row)] == "." for i, x in enumerate(row)]
            changed = changed or any(can_move)
            new_data.append(["." if x else arrow if can_move[(i - 1) % len(row)] else row[i]
                             for i, x in enumerate(can_move)])
        self.data = new_data if direction == "east" else transpose(new_data)
        return changed

    def find_gridlock(self):
        i = 1
        while self.move():
            i += 1
        return i


def transpose(x: List[list]) -> List[list]:
    """Transpose a list of lists (doesn't check for appropriate dimensions)"""
    return list(map(list, zip(*x)))


def parse_data(path: str) -> List[List[str]]:
    data: List[str] = read_text_file(path)
    return [list(x) for x in data]


if __name__ == "__main__":
    data = parse_data("data/25.txt")

    ### Part 1
    grid = Grid(data)
    solution = grid.find_gridlock()
    print(f"Solution 25a: {solution}")
