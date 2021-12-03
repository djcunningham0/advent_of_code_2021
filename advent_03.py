from shared import read_text_file
from typing import List


def get_most_common_digit_all_columns(data: List[str]) -> str:
    """
    Given a list of n-digit binary numbers, get the most common digit in each of the n
    places. Return the result in a single string. For example, if the input is:
    "10010"
    "01010"
    "00011"

    The output would be "00010".
    """
    # assume all entries are the same length, and only "0" and "1" appear so we can sum
    n_columns = len(data[0])
    out_digits = [get_most_common_digit_single_column(data, i) for i in range(n_columns)]
    return "".join(out_digits)


def get_most_common_digit_single_column(data: List[str], index: int) -> str:
    col_sum = sum(int(x[index]) for x in data)
    return str(int(col_sum >= len(data) / 2))  # return "1" if equally common


def flip_binary_digits(x: str) -> str:
    """Flip 0s to 1s and 1s to 0s. Example: 100010 --> 011101"""
    return "".join([str(int(not int(z))) for z in x])


def binary_to_decimal(x: str) -> int:
    return int(x, 2)


def get_oxygen_rating(data: List[str]) -> int:
    x = recursive_filter(data)
    return binary_to_decimal(x)


def get_co2_rating(data: List[str]) -> int:
    x = recursive_filter(data, least=True)
    return binary_to_decimal(x)


def recursive_filter(data: List[str], current_index: int = 0, least: bool = False) -> str:
    """Recursively filter the data until only one value is left -- then return it."""
    if len(data) == 1:
        return data[0]
    else:
        data = filter_to_digit(data, index=current_index, least=least)
        return recursive_filter(data, current_index + 1, least)


def filter_to_digit(data: List[str], index: int, least: bool = False) -> List[str]:
    """
    Filter the data to only include values that have the most (or least) common value
    in the specified column.
    """
    digit = get_most_common_digit_single_column(data, index)
    if least:
        digit = flip_binary_digits(digit)
    return [x for x in data if x[index] == digit]


if __name__ == "__main__":
    data = read_text_file("data/03.txt", dtype=str)

    ### Part 1
    gamma = get_most_common_digit_all_columns(data)
    epsilon = flip_binary_digits(gamma)
    gamma = binary_to_decimal(gamma)
    epsilon = binary_to_decimal(epsilon)
    print(f"solution 03a: {gamma * epsilon}")

    ### Part 2
    oxygen_rating = get_oxygen_rating(data)
    co2_rating = get_co2_rating(data)
    print(f"solution 03b: {oxygen_rating * co2_rating}")
