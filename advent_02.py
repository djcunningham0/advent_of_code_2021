from shared import read_text_file
from typing import List, Tuple


def get_depth_and_horizontal_coordinates(data: List[str]) -> Tuple[int, int]:
    """
    Get depth and horizontal position after a series of commands like "down 2",
    "forward 5", "up 1", etc.
    """
    depth, horizontal = 0, 0
    for direction in data:
        coords = process_direction(direction)
        depth += coords[0]
        horizontal += coords[1]
    return depth, horizontal


def process_direction(x: str) -> Tuple[int, int]:
    """
    Return the change to (depth, horizontal) coordinates from a direction like "down 2",
    "forward 5", "up 1", etc.
    """
    map = {
        "down": (1, 0),
        "up": (-1, 0),
        "forward": (0, 1),
    }
    d, n = x.split(" ")  # separate the direction and number of units
    n = int(n)
    return map[d][0] * n, map[d][1] * n


def get_depth_and_horizontal_coordinates_with_aim(data: List[str]) -> Tuple[int, int]:
    """
    Get depth and horizontal position after a series of commands like "down 2",
    "forward 5", "up 1", etc. Now down an up update the aim, and forward adjusts both
    depth and horizontal.
    """
    depth, horizontal, aim = 0, 0, 0
    for direction in data:
        update = update_coordinates_and_aim(direction, aim)
        depth += update[0]
        horizontal += update[1]
        aim += update[2]
    return depth, horizontal


def update_coordinates_and_aim(direction: str, current_aim: int) -> Tuple[int, int, int]:
    """
    Return the change to (depth, horizontal, aim) coordinates from a direction like "down 2",
    "forward 5", "up 1", etc.
    """
    # changes to (depth, horizontal, aim)
    map = {
        "down": (0, 0, 1),
        "up": (0, 0, -1),
        "forward": (current_aim, 1, 0),
    }
    d, n = direction.split(" ")  # separate the direction and number of units
    n = int(n)
    return map[d][0] * n, map[d][1] * n, map[d][2] * n


if __name__ == "__main__":
    data = read_text_file("data/02.txt", dtype=str)

    ### Part 1
    coords = get_depth_and_horizontal_coordinates(data)
    print(f"solution 02a: {coords[0] * coords[1]}")

    ### Part 2
    coords = get_depth_and_horizontal_coordinates_with_aim(data)
    print(f"solution 02b: {coords[0] * coords[1]}")
