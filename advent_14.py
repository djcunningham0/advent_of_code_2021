from shared import read_text_file
from collections import Counter
from typing import Tuple, Dict


def parse_data(path: str) -> Tuple[str, Dict[str, str]]:
    data = read_text_file(path)
    template = data[0]
    rules = dict(x.split(" -> ") for x in data[2:])
    return template, rules


def process_rules(pair_counts: Counter[str, int], rules: Dict[str, str]) -> Counter[str, int]:
    new_pair_counts = Counter()
    for pair, count in pair_counts.items():
        try:
            # if it matches a rule, all of these pairs turn into the new pairs
            new_pair_1 = f"{rules[pair]}{pair[1]}"
            new_pair_2 = f"{pair[0]}{rules[pair]}"
            new_pair_counts[new_pair_1] += count
            new_pair_counts[new_pair_2] += count
        except KeyError:
            # otherwise we keep the existing pairs
            new_pair_counts[pair] += count
    return new_pair_counts


def string_to_pair_counts(s: str) -> Counter[str, int]:
    """Take a string and return a dict counting the occurrences of each pair."""
    s = f"_{s}_"  # pad so we can keep track of the start and end characters correctly
    c = Counter()
    for pair in [s[i:i+2] for i in range(len(s)-1)]:
        c[pair] += 1
    return c


def process_rules_n_times(s: str, rules: Dict[str, str], n: int) -> Counter[str, int]:
    pair_counts = string_to_pair_counts(s)
    for _ in range(n):
        pair_counts = process_rules(pair_counts, rules)
    return pair_counts


def pair_counts_to_letter_counts(pair_counts: Counter[str, int]) -> Counter[str, int]:
    letter_counts = Counter()
    for pair, count in pair_counts.items():
        letter_counts[pair[0]] += count / 2  # over 2 because we'll encounter the letter in both positions of the pair
        letter_counts[pair[1]] += count / 2
    letter_counts.pop("_")
    return letter_counts


if __name__ == "__main__":
    template, rules = parse_data("data/14.txt")

    ### Part 1
    pair_counts = process_rules_n_times(template, rules, 10)
    letter_counts = pair_counts_to_letter_counts(pair_counts)
    solution = max(letter_counts.values()) - min(letter_counts.values())
    print(f"Solution 14a: {int(solution)}")

    ### Part 2
    pair_counts = process_rules_n_times(template, rules, 40)
    letter_counts = pair_counts_to_letter_counts(pair_counts)
    solution = max(letter_counts.values()) - min(letter_counts.values())
    print(f"Solution 14b: {int(solution)}")

