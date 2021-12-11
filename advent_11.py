from shared import read_text_file
import itertools
from math import inf
from typing import List, Generator, Tuple


def parse_data(path: str) -> List[List[int]]:
    data = read_text_file(path)
    return [[int(x) for x in line] for line in data]


class Grid:
    def __init__(self, data: List[List[int]]):
        self.data = data.copy()
        assert all(len(x) == len(data[0]) for x in data)
        self.n_rows = len(data)
        self.n_columns = len(data[0])
        self.pad_data()
        self.flash_count = 0
        self.time_step = 0

    def all_points(self) -> Generator[Tuple[int, int], None, None]:
        for x in itertools.product(range(1, self.n_rows + 1), range(1, self.n_columns + 1)):
            yield x

    def advance_one_step(self) -> int:
        """Advance one time step. Return the flash count for this step."""
        self.time_step += 1
        self.increment_all_points()
        return self.process_flashes()

    def advance_n_steps(self, n: int):
        """Advance n time steps."""
        for _ in range(n):
            self.advance_one_step()

    def pad_data(self):
        """Surround all the data with negative infinity to make it easier to increment
        surrounding values."""
        self.data.insert(0, [-inf] * self.n_columns)
        self.data.append([-inf] * self.n_columns)
        self.data = [[-inf] + x + [-inf] for x in self.data]

    def increment_all_points(self):
        for i, j in self.all_points():
            self.increment_point(i, j)

    def increment_point(self, i: int, j: int):
        self.data[i][j] += 1

    def process_flashes(self, _step_flash_count: int = 0) -> int:
        """
        Flash any points > 9, then increment surrounding points and continue until no
        more flashes. Return the total flash count.
        """
        new_flashes = 0
        for i, j in self.all_points():
            if self.data[i][j] > 9:
                new_flashes += 1
                self.data[i][j] = -inf  # temporarily set to -infinity so it can't flash again this round
                self.increment_surrounding_points(i, j)
        # if there were flashes, some surrounding points were incremented and there might be new flashes to count
        if new_flashes > 0:
            self.flash_count += new_flashes
            _step_flash_count += new_flashes
            return self.process_flashes(_step_flash_count)
        else:
            # reset the flashed points from -inf to zero
            for i, j in self.all_points():
                self.data[i][j] = max(0, self.data[i][j])
            return _step_flash_count

    def increment_surrounding_points(self, i, j):
        self.data[i-1][j-1] += 1
        self.data[i-1][j] += 1
        self.data[i-1][j+1] += 1
        self.data[i][j-1] += 1
        self.data[i][j+1] += 1
        self.data[i+1][j-1] += 1
        self.data[i+1][j] += 1
        self.data[i+1][j+1] += 1

    def find_first_all_flash(self):
        if self.advance_one_step() == self.n_rows * self.n_columns:
            return self.time_step
        else:
            return self.find_first_all_flash()

    def __repr__(self):
        out = ""
        for line in self.data:
            out += "\n" + "\t" + str(line)
        return f"Grid({out}\n)"


if __name__ == "__main__":
    data = parse_data("data/11.txt")

    ### Part 1
    grid = Grid(data)
    grid.advance_n_steps(100)
    print(f"Solution 11a: {grid.flash_count}")

    ### Part 2
    grid = Grid(data)
    solution = grid.find_first_all_flash()
    print(f"Solution 11b: {solution}")
