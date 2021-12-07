from shared import read_text_file
from statistics import median
from typing import List, Tuple, Callable


def parse_data(path: str):
    return [int(x) for x in read_text_file(path, dtype=str)[0].split(",")]


def get_min_position_and_distance(values: List[int], distance_function: Callable = None) -> Tuple[int, int]:
    if not distance_function:
        # the median minimizes euclidean distance: https://en.wikipedia.org/wiki/Geometric_median
        m = median(values)
        return m, sum(abs(x - m) for x in values)
    else:
        # otherwise calculate with brute force
        d = dict()
        for i in range(min(values), max(values)):
            d[i] = sum(distance_function(x, i) for x in values)
        argmin = min(d, key=d.get)
        return argmin, d[argmin]


def triangle_number_distance(a: int, b: int):
    """Distances in part 2 are triangle numbers: https://en.wikipedia.org/wiki/Triangular_number"""
    return triangle_number(abs(a - b))


def triangle_number(n: int):
    return n * (n + 1) / 2


if __name__ == "__main__":
    data = parse_data("data/07.txt")

    ### Part 1
    x, dist = get_min_position_and_distance(data)
    print(f"solution 07a: {dist}")

    ### Part 2
    x, dist = get_min_position_and_distance(data, distance_function=triangle_number_distance)
    print(f"solution 07b: {dist}")
