from shared import read_text_file
from typing import List, Any


START_BRACKETS = ["(", "[", "{", "<"]
END_BRACKETS = [")", "]", "}", ">"]
BRACKET_DICT = dict(zip(START_BRACKETS, END_BRACKETS))
CORRUPT_SCORE_DICT = {")": 3, "]": 57, "}": 1197, ">": 25137}
INCOMPLETE_SCORE_DICT = {")": 1, "]": 2, "}": 3, ">": 4}


def parse_data(path: str) -> List[str]:
    return read_text_file(path)


def find_corrupting_character_one_line(line: str) -> str:
    open_brackets = []
    for char in line:
        if char in START_BRACKETS:
            open_brackets.append(char)
        elif char != BRACKET_DICT[open_brackets[-1]]:
            return char
        else:
            open_brackets.pop(-1)  # we closed a bracket correctly, so remove it from the open list


def find_corrupting_characters(data: List[str]) -> List[str]:
    return [find_corrupting_character_one_line(line) for line in data]


def score_corrupting_characters(chars: List[str]) -> int:
    return sum(CORRUPT_SCORE_DICT.get(x, 0) for x in chars)


def filter_to_incomplete_lines(data: List[str]) -> List[str]:
    return [x for x in data if find_corrupting_character_one_line(x) is None]


def get_completing_characters_one_line(line: str) -> str:
    open_brackets = []
    for char in line:
        if char in START_BRACKETS:
            open_brackets.append(char)
        elif char == BRACKET_DICT[open_brackets[-1]]:
            open_brackets.pop(-1)  # we closed a bracket correctly, so remove it from the open list
        else:
            # should never reach this unless we call the function on the wrong data
            raise ValueError(f"found corrupt character: {char}")
    return "".join([BRACKET_DICT[x] for x in open_brackets[::-1]])


def get_completing_characters(data: List[str]) -> List[str]:
    data = filter_to_incomplete_lines(data)
    return [get_completing_characters_one_line(line) for line in data]


def score_completing_characters_one_line(chars: str) -> int:
    score = 0
    for char in chars:
        score = score * 5 + INCOMPLETE_SCORE_DICT[char]
    return score


def score_completing_characters(chars: List[str]) -> List[int]:
    return [score_completing_characters_one_line(x) for x in chars]


def get_middle_item(x: list) -> Any:
    return sorted(x)[len(x) // 2]


if __name__ == "__main__":
    data = read_text_file("data/10.txt")

    ### Part 1
    chars = find_corrupting_characters(data)
    score = score_corrupting_characters(chars)
    print(f"Solution 10a: {score}")

    ### Part 2
    chars = get_completing_characters(data)
    scores = score_completing_characters(chars)
    middle_score = get_middle_item(scores)
    print(f"Solution 10b: {middle_score}")
