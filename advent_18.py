"""
This solution is pretty inefficient because I did a lot of string parsing rather than
work directly with the nested lists. It takes about 15 seconds to run on the full data
on my computer.
"""

from shared import read_text_file
import ast
import math
from itertools import product
from typing import Generator, List


class Number:
    def __init__(self, x: list):
        self.x = x
        assert 1 <= list_depth(x) <= 4 or self.x == []  # otherwise it's not a valid number

    def __add__(self, other):
        if self.x == []:
            return other
        elif other.x == []:
            return self
        new_x = [self.x, other.x]
        while list_depth(new_x) > 4 or get_max_value_in_nested_list(new_x) >= 10:
            if list_depth(new_x) > 4:
                new_x = explode(new_x)
            else:
                new_x = split(new_x)
        return Number(new_x)

    def __eq__(self, other):
        return self.x == other.x

    def __repr__(self):
        return f"Number({self.x})"


def list_depth(x: list) -> int:
    if isinstance(x, list):
        return 1 + max(list_depth(item) for item in x) if len(x) > 0 else 0
    else:
        return 0


def is_number(x: str) -> bool:
    try:
        int(x)
        return True
    except ValueError:
        return False


def explode(int_list: list) -> list:
    str_list = str(int_list).replace(" ", "")
    depth = 0
    prev_num = ("", "")  # loc, value
    left = ("", "")
    right = ("", "")
    next_num = ("", "")
    skip = False
    for i, x in enumerate(str_list):
        if left[1] != "" and right[1] != "" and next_num[1] != "":
            break
        if skip:
            skip = False
            continue
        skip = False
        if x == "[":
            depth += 1
        elif x == "]":
            depth -= 1
        elif is_number(x):
            if is_number(str_list[i+1]):
                # check if it's a two-digit number (making the assumption of no three-digit numbers)
                skip = True
                x = f"{x}{str_list[i+1]}"

            if depth < 5 or right[1] != "":
                if left == ("", ""):
                    prev_num = (i, x)
                else:
                    next_num = (i, x)
            else:
                if left == ("", ""):
                    left = (i, x)
                else:
                    right = (i, x)

    out = ""
    if prev_num[1]:
        new_val = int(prev_num[1]) + int(left[1])
        out = f"{str_list[:prev_num[0]]}{new_val}"
    prev_adj = 2 if len(prev_num[1]) > 1 else 1 if len(prev_num[1]) == 1 else 0
    start = (prev_num[0] or 0) + prev_adj
    end = left[0] - 1
    out = f"{out}{str_list[start:end]}0"
    right_adj = 3 if len(right[1]) > 1 else 2
    start = right[0] + right_adj
    end = next_num[0] or len(str_list) + 1
    out = f"{out}{str_list[start:end]}"
    if next_num[1]:
        new_val = int(right[1]) + int(next_num[1])
        next_adj = 2 if len(next_num[1]) > 1 else 1
        out = f"{out}{new_val}{str_list[next_num[0] + next_adj:]}"

    return ast.literal_eval(out)


def split(int_list: list) -> list:
    str_list = str(int_list).replace(" ", "")
    for i, x in enumerate(str_list):
        if not is_number(x) or not is_number(str_list[i + 1]):
            # find the first two-digit number (note: this won't work if we encounter three-digit numbers)
            continue
        x = int(f"{x}{str_list[i + 1]}")
        return ast.literal_eval(f"{str_list[:i]}[{math.floor(x/2)},{math.ceil(x/2)}]{str_list[i+2:]}")


def flatten_list(x: list) -> Generator[list, None, None]:
    for y in x:
        if isinstance(y, list):
            yield from flatten_list(y)
        else:
            yield y


def get_max_value_in_nested_list(x: list) -> int:
    return max(flatten_list(x))


def sum_numbers(x: List[Number]) -> Number:
    return sum(x, start=Number([]))


def get_magnitude(n: Number) -> int:
    str_list = str(n.x).replace(" ", "")
    while str_list.startswith("[") and str_list.endswith("]"):
        skip = 0
        left = ("", "")
        right = ("", "")
        for i, x in enumerate(str_list):
            # find first appearance of [number, number]
            if left[1] != "" and right[1] != "":
                break
            if skip:
                skip -= 1
                continue
            if x in ["[", "]"]:
                left = ("", "")
                right = ("", "")
            if is_number(x):
                if is_number(str_list[i + 1]):
                    # check for 2-, 3-, and 4-digit numbers (should do this smarter, but I'm being lazy)
                    x = f"{x}{str_list[i + 1]}"
                    skip += 1
                    if is_number(str_list[i + 2]):
                        x = f"{x}{str_list[i + 2]}"
                        skip += 1
                        if is_number(str_list[i + 3]):
                            x = f"{x}{str_list[i + 3]}"
                            skip += 1
                if left[1] == "":
                    left = (i, x)
                else:
                    right = (i, x)

        val = 3 * int(left[1]) + 2 * int(right[1])
        right_adj = len(right[1]) + 1
        str_list = f"{str_list[:left[0]-1]}{val}{str_list[right[0] + right_adj:]}"

    return int(str_list)


def get_pairwise_magnitudes(number_list: List[Number]) -> List[int]:
    magnitudes = []
    for n1, n2 in product(number_list, number_list):
        if n1 == n2:
            continue
        n = n1 + n2
        magnitudes.append(get_magnitude(n))
    return magnitudes


def parse_data(path: str) -> List[Number]:
    data = read_text_file(path)
    data = [Number(ast.literal_eval(x)) for x in data]
    return data


if __name__ == "__main__":
    data = parse_data("data/18.txt")

    ### Part 1
    n = sum_numbers(data)
    magnitude = get_magnitude(n)
    print(f"Solution 18a: {magnitude}")

    ### Part 2
    magnitudes = get_pairwise_magnitudes(data)
    print(f"Solution 18b: {max(magnitudes)}")
