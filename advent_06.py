from __future__ import annotations  # this just allows type hinting a class method to return the same class

from shared import read_text_file
from typing import List, Any


CYCLE_LENGTH = 7
NEW_FISH_EXTRA = 2


def rotate_list(x: List[Any]) -> List[Any]:
    """
    Rotate the elements in a list by one position.
    Example:
    >>> rotate_list([1, 2, 3, 4, 5])
    [2, 3, 4, 5, 1]
    """
    return x[1:] + x[:1]


class FishTank:
    def __init__(self, data: List[int]):
        # counts[i] contains the number of fish with timer == i
        self.counts = [data.count(i) for i in range(CYCLE_LENGTH + NEW_FISH_EXTRA)]

    def advance_n_days(self, n: int):
        """
        Rotate counts because each fish becomes one day closer to reproducing. Fish with
        zero days left produce new fish with the max value (handled by the rotation) and
        need to be reset to CYCLE_LENGTH (handled by adding to the appropriate count).
        """
        for _ in range(n):
            self.counts = rotate_list(self.counts)
            self.counts[CYCLE_LENGTH - 1] += self.counts[CYCLE_LENGTH + NEW_FISH_EXTRA - 1]

    def count_fish(self):
        return sum(self.counts)


def parse_data(path: str) -> List[int]:
    data = read_text_file(path, dtype=str)
    return [int(x) for x in data[0].split(",")]


if __name__ == "__main__":
    data = parse_data("data/06.txt")

    ### Part 1
    tank = FishTank(data=data)
    tank.advance_n_days(80)
    print(f"solution 06a: {tank.count_fish()}")

    ### Part 2
    tank = FishTank(data=data)
    tank.advance_n_days(256)
    print(f"solution 06b: {tank.count_fish()}")
