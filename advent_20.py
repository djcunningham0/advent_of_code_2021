from shared import read_text_file
from itertools import product
from copy import deepcopy
from typing import List


class Image:
    def __init__(self, data: List[List[str]], algorithm: str):
        self.data = data
        self.algorithm = algorithm
        self.border_value = "."

    def enhance(self):
        self._add_border()
        n_rows = len(self.data)
        n_cols = len(self.data[0])
        new_data = deepcopy(self.data)
        for i, j in product(range(n_rows), range(n_cols)):
            index = self.get_pixel_output(i, j)
            new_data[i][j] = self.algorithm[index]
        self.data = new_data

        # the infinite surrounding pixels all get set to the first or last value in the algorithm
        self.border_value = self.algorithm[0] if self.border_value == "." else self.algorithm[-1]

    def multi_enhance(self, n: int):
        for _ in range(n):
            self.enhance()

    def get_pixel_output(self, i: int, j: int) -> int:
        max_row = len(self.data) - 1
        max_col = len(self.data[0]) - 1
        topleft = self.data[i - 1][j - 1] if i > 0 and j > 0 else self.border_value
        topmid = self.data[i - 1][j] if i > 0 else self.border_value
        topright = self.data[i - 1][j + 1] if i > 0 and j < max_col else self.border_value
        midleft = self.data[i][j - 1] if j > 0 else self.border_value
        midmid = self.data[i][j]
        midright = self.data[i][j + 1] if j < max_col else self.border_value
        botleft = self.data[i + 1][j - 1] if i < max_row and j > 0 else self.border_value
        botmid = self.data[i + 1][j] if i < max_row else self.border_value
        botright = self.data[i + 1][j + 1] if i < max_row and j < max_col else self.border_value
        pixel_string = f"{topleft}{topmid}{topright}{midleft}{midmid}{midright}{botleft}{botmid}{botright}"
        binary_value = pixel_string.replace(".", "0").replace("#", "1")
        return int(binary_value, 2)

    def count_lit_pixels(self):
        return sum(x.count("#") for x in self.data)

    def _add_border(self):
        """Add a border of dark pixels"""
        n_cols = len(self.data[0])
        self.data.insert(0, [self.border_value] * n_cols)
        self.data.append([self.border_value] * n_cols)
        n_rows = len(self.data)
        for i in range(n_rows):
            self.data[i] = [self.border_value, *self.data[i], self.border_value]

    def __repr__(self):
        out = "\n\t".join("".join(x) for x in self.data)
        return f"Image(\n\t{out}\n)"


def parse_data(path: str) -> Image:
    data: List[str] = read_text_file(path)
    algorithm = data[0]
    image = [list(x) for x in data[2:]]
    return Image(image, algorithm)


if __name__ == "__main__":
    image = parse_data("data/20.txt")

    ### Part 1
    image.multi_enhance(2)
    print(f"Solution 20a: {image.count_lit_pixels()}")

    ### Part 2
    image = parse_data("data/20.txt")
    image.multi_enhance(50)
    print(f"Solution 20b: {image.count_lit_pixels()}")
