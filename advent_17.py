from shared import read_text_file
from typing import List, Tuple, Optional
from itertools import product


class Target:
    def __init__(self, xmin: int, xmax: int, ymin: int, ymax: int):
        self.xmin = min(xmin, xmax)
        self.xmax = max(xmin, xmax)
        self.ymin = min(ymin, ymax)
        self.ymax = max(ymin, ymax)

    def find_solutions(self) -> List[Tuple[int, int, int]]:
        viable_x = self.get_viable_x_velocities()
        viable_y = self.get_viable_y_velocities()
        solutions = []
        for xvel, yvel in product(viable_x, viable_y):
            height = self.try_initial_conditions(xvel, yvel)
            if height is not None:
                solutions.append((xvel, yvel, height))
        return solutions

    def find_max_height(self) -> int:
        return max(self.find_solutions(), key=lambda x: x[2])[2]

    def try_initial_conditions(self, xvel: int, yvel: int) -> Optional[int]:
        """If the conditions work, return the max height. Otherwise return nothing."""
        x, y = 0, 0
        max_height = 0
        while x <= self.xmax and y >= self.ymin:
            max_height = max(max_height, y)
            if (x, y) in self:
                return max_height
            x += xvel
            y += yvel
            xvel = xvel - 1 if xvel > 0 else xvel + 1 if xvel < 0 else 0
            yvel -= 1

    def get_viable_x_velocities(self) -> List[int]:
        """Return tuples of (velocity, time step) for all viable x velocities."""
        out = []
        for xvel in range(self.xmax + 1):
            velocities = range(xvel, 0, -1)
            x_vals = [sum(velocities[:i + 1]) for i in range(len(velocities))]
            if any(self.xmin <= x <= self.xmax for x in x_vals):
                out.append(xvel)
        return out

    def get_viable_y_velocities(self) -> List[int]:
        # note: this probably only works for targets with ymin and ymax less than zero
        out = []
        min_vel = self.ymin
        max_vel = -self.ymin  # the (n*2)th position will be zero, and the next will be target.ymin
        for yvel in range(min_vel, max_vel + 1):
            y = 0
            vel = yvel
            done = False
            while y >= self.ymin and not done:
                if self.ymin <= y <= self.ymax:
                    out.append(yvel)
                    done = True
                else:
                    y += vel
                    vel -= 1
        return out

    def __contains__(self, point: Tuple[int, int]) -> bool:
        return self.xmin <= point[0] <= self.xmax and self.ymin <= point[1] <= self.ymax

    def __repr__(self):
        return f"Target({self.xmin}, {self.xmax}, {self.ymin}, {self.ymax})"


def parse_data(path: str) -> Target:
    data: str = read_text_file(path)[0]
    x = data.split("x=")[1].split(",")[0]
    xmin, xmax = x.split("..")
    y = data.split("y=")[1].split(",")[0]
    ymin, ymax = y.split("..")
    return Target(int(xmin), int(xmax), int(ymin), int(ymax))


if __name__ == "__main__":
    target = parse_data("data/17.txt")
    # target = parse_data("tests/data/17.txt")

    ### Part 1
    max_height = target.find_max_height()
    print(f"Solution 1: {max_height}")

    ### Part 2
    print(f"Solution 2: {len(target.find_solutions())}")
