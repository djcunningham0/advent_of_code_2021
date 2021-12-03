from shared import read_text_file
from typing import List


def get_diffs(x: List[float]) -> List[float]:
    """Get the differences between subsequent elements in a list."""
    return [x[i] - x[i-1] for i in range(1, len(x))]


def count_diffs_greater_than_zero(x: List[float]) -> int:
    """Count the number of diffs that are greater than zero in a list."""
    diffs = get_diffs(x)
    return sum(x > 0 for x in diffs)


def get_rolling_sums(x: List[float], n: int) -> List[float]:
    """Get the rolling sums in a list with a window of size n."""
    return [sum(x[i:i+n]) for i in range(len(x)-n+1)]


if __name__ == "__main__":
    data = read_text_file("data/01.txt", dtype=int)

    ### Part 1
    n = count_diffs_greater_than_zero(data)
    print(f"solution 01a: {n}")

    ### Part 2
    rolling_sums = get_rolling_sums(data, 3)
    n = count_diffs_greater_than_zero(rolling_sums)
    print(f"solution 01b: {n}")
