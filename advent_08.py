"""
This one isn't particularly optimized and I'm basically doing part 2 by brute force.
It's the slowest running solution so far. (It still runs in less han a second on my
machine -- 2020 MacBook Air).
"""

from shared import read_text_file
from typing import List, Tuple, Generator, Set
from itertools import permutations


DIGIT_MAP = [
    {"a", "b", "c", "e", "f", "g"},  # 0
    {"c", "f"},  # 1
    {"a", "c", "d", "e", "g"},  # 2
    {"a", "c", "d", "f", "g"},  # 3
    {"b", "c", "d", "f"},  # 4
    {"a", "b", "d", "f", "g"},  # 5
    {"a", "b", "d", "e", "f", "g"},  # 6
    {"a", "c", "f"},  # 7
    {"a", "b", "c", "d", "e", "f", "g"},  # 8
    {"a", "b", "c", "d", "f", "g"},  # 9
]


def parse_data(path: str) -> Tuple[List[str], List[str]]:
    data = read_text_file(path, dtype=str)
    split_data = [x.split(" | ") for x in data]
    input, output = [x[0] for x in split_data], [x[1] for x in split_data]
    return input, output


def count_easy_digits(strings: List[str]) -> int:
    return sum(_count_easy_digits_one_string(x) for x in strings)


def _count_easy_digits_one_string(string: str) -> int:
    easy_digit_lengths = {2, 3, 4, 7}
    lengths = [len(x) for x in string.split(" ")]
    return sum(x in easy_digit_lengths for x in lengths)


class LetterMap:
    def __init__(self, order: Tuple[str]):
        # map takes the observed digit and translates to what it should be
        self.map = {
            order[0]: "a",
            order[1]: "b",
            order[2]: "c",
            order[3]: "d",
            order[4]: "e",
            order[5]: "f",
            order[6]: "g",
        }

    def map_digit_string(self, digit_string: str) -> Set[str]:
        return set(self.map[x] for x in digit_string)

    def is_valid_for_digit_string(self, digit_string: str) -> bool:
        return self.map_digit_string(digit_string) in DIGIT_MAP

    def is_valid_for_line(self, line: str) -> bool:
        return all(self.is_valid_for_digit_string(x) for x in line.split(" "))

    def evaluate_digit_string(self, digit_string: str) -> str:
        return str(DIGIT_MAP.index(self.map_digit_string(digit_string)))

    def evaluate_line(self, line: str) -> int:
        digit_strings = [x for x in line.split(" ")]
        digits = [self.evaluate_digit_string(x) for x in digit_strings]
        return int("".join(digits))


def generate_candidate_maps() -> Generator[LetterMap, None, None]:
    """
    Map each observed letter to some real letter. Dictionary keys are the observed
    letters in the string, and the values are the letters we'll try mapping them to.
    """
    for order in permutations({"a", "b", "c", "d", "e", "f", "g"}):
        yield LetterMap(order)


def find_valid_map_for_line(line: str) -> LetterMap:
    for i, letter_map in enumerate(generate_candidate_maps()):  # TODO remove enumerate
        if letter_map.is_valid_for_line(line):
            return letter_map
    raise ValueError("did not find a valid map")  # should never reach this point


def find_all_valid_maps(data: List[str]) -> List[LetterMap]:
    return [find_valid_map_for_line(line) for line in data]


def evaluate_all_maps(maps: List[LetterMap], data: List[str]) -> int:
    return sum(m.evaluate_line(line) for m, line in zip(maps, data))


if __name__ == "__main__":
    input, output = parse_data("data/08.txt")

    ### Part 1
    n = count_easy_digits(output)
    print(f"Solution 08a: {n}")

    ### Part 2
    maps = find_all_valid_maps(input)
    solution = evaluate_all_maps(maps, output)
    print(f"Solution 08b: {solution}")
