"""
Not the most satisfying solution. It's basically brute force, though a little more
clever than the obvious brute force approach of trying all possible numbers (which is
not practical).

Each part takes about 12 seconds and that's after somewhat arbitrarily pruning branches
when the z value becomes very large. I bumped up the prune threshold until it produced
a valid solution, which fortunately was correct. It's possible that this script wouldn't
work for some inputs.

Caching the process_instruction function helped a little bit, but not much. I don't know
if there's anywhere else caching would help. It would be possible to parallelize parts
of the code, but I'm not going to bother.

It might be faster to solve this one by studying the instructions and maybe even working
it out by hand... I didn't try that.
"""

from shared import read_text_file
from typing import List, Tuple
from math import inf
from collections import defaultdict
from functools import cache


VAR_MAP = {"w": 0, "x": 1, "y": 2, "z": 3}


def solve(instructions: List[Tuple[str]], min_val: bool = False, prune_threshold: int = inf):
    """
    Start at (0, 0, 0, 0). Process from the first input to the second input using inputs
    1 through 9. Record the distinct (w, x, y, z) states that can be reached and the max
    (or min) input that reached that state. Then process from the second input to the
    third starting from all possible states reached on the previous step for input
    values 1 through 9. Repeat for all input steps. Finally, filter to all ending states
    where z == 0 and select the maximum value.
    """
    if min_val:
        def check(new: int, existing: int) -> bool:
            return new < existing
    else:
        def check(new: int, existing: int) -> bool:
            return new > existing
    states = {(0, 0, 0, 0): inf if min_val else 0}  # (w, x, y, z): max_input or min_input
    for i, inst in enumerate(split_instructions(instructions)):
        new_states = defaultdict(lambda: inf if min_val else 0)
        for state, prev_input in states.items():
            for input_ in range(9, 0, -1):
                new_state = process_multiple_instructions(inst, state, input_)
                full_input = int(f"{prev_input}{input_}") if prev_input != inf else input_
                if abs(new_state[3]) < prune_threshold:
                    if check(full_input, new_states[new_state]):
                        new_states[new_state] = full_input
        states = new_states

    solutions = {k: v for k, v in states.items() if k[3] == 0}
    if min_val:
        return min(solutions.values())
    else:
        return max(solutions.values())


def split_instructions(instructions: List[Tuple[str]]) -> List[List[Tuple[str]]]:
    """Split by input commands"""
    input_indices = [i for i, x in enumerate(instructions) if x[0] == "inp"]
    input_indices += [len(instructions) + 1]
    return [instructions[x:input_indices[i+1]] for i, x in enumerate(input_indices[:-1])]


@cache
def process_instruction(
        instruction: Tuple[str],
        current_vals: Tuple[int, int, int, int],
        input_value: int = None,
) -> Tuple[int, int, int, int]:
    command = instruction[0]
    var = instruction[1]
    index = VAR_MAP[var]
    if command == "inp":
        value = int(input_value)
        new_vals = tuple_replace(current_vals, index, value)
    else:
        value = instruction[2]
        try:
            value = int(value)
        except ValueError:
            val_index = VAR_MAP[value]
            value = current_vals[val_index]

        if command == "add":
            new_vals = tuple_replace(current_vals, index, current_vals[index] + value)
        elif command == "mul":
            new_vals = tuple_replace(current_vals, index, current_vals[index] * value)
        elif command == "div":
            new_vals = tuple_replace(current_vals, index, current_vals[index] // value)
        elif command == "mod":
            new_vals = tuple_replace(current_vals, index, current_vals[index] % value)
        elif command == "eql":
            new_vals = tuple_replace(current_vals, index, 1 if current_vals[index] == value else 0)
        else:
            raise ValueError(f"Invalid command: {command}")

    return new_vals


def process_multiple_instructions(
        instructions: List[Tuple[str]],
        current_vals: Tuple[int, int, int, int],
        input_value: int = None,
) -> Tuple[int, int, int, int]:
    for i in instructions:
        current_vals = process_instruction(i, current_vals, input_value)
    return current_vals


def tuple_replace(t: tuple, index: int, value) -> tuple:
    return t[:index] + tuple([value]) + t[index + 1:]


def parse_data(path: str) -> List[Tuple[str]]:
    data = read_text_file(path)
    return [tuple(x.split()) for x in data]


if __name__ == "__main__":
    data = parse_data("data/24.txt")

    ### Part 1
    solution = solve(data, prune_threshold=1e6)
    print(f"Solution 24a: {solution}")

    ### Part 2
    solution = solve(data, min_val=True, prune_threshold=1e6)
    print(f"Solution 24b: {solution}")
