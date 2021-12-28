from shared import read_text_file
from typing import Tuple, List, Generator
from itertools import product
from functools import cache


class Die:
    def __init__(self, max_val: int = 100):
        def g() -> Generator[int, None, None]:
            x = 0
            while True:
                yield x % max_val + 1
                x += 1

        self.g = g()
        self.n_rolls = 0

    def roll(self) -> int:
        self.n_rolls += 1
        return next(self.g)

    def roll_n(self, n: int) -> int:
        return sum([self.roll() for _ in range(n)])


class Game:
    def __init__(self, p0: int, p1: int, s0: int = 0, s1: int = 0, current_turn: int = 0, winning_score: int = 1000):
        self.positions = [p0, p1]
        self.scores = [s0, s1]
        self.die = Die()
        self.current_turn = current_turn
        self.winning_score = winning_score

    def play(self):
        while max(self.scores) < self.winning_score:
            total_roll = self.die.roll_n(3)
            self.advance_one_turn(total_roll)

    def advance_one_turn(self, total_roll: int):
        player = self.current_turn
        new_position = self.get_new_position(self.positions[player], total_roll)
        self.positions[player] = new_position
        self.scores[player] += new_position
        self._toggle_turn()

    @staticmethod
    def get_new_position(current_space: int, n_spaces: int) -> int:
        return (current_space + n_spaces - 1) % 10 + 1

    def _toggle_turn(self):
        self.current_turn = (self.current_turn + 1) % 2

    def __repr__(self):
        return f"Game({self.scores[0]}-{self.scores[1]}; positions {self.positions[0]}, {self.positions[1]})"


DIRAC_ROLLS = [sum(x) for x in product([1, 2, 3], [1, 2, 3], [1, 2, 3])]


@cache
def get_win_counts(p0: int, p1: int, s0: int = 0, s1: int = 0, turn: int = 0) -> List[int]:
    win_counts = [0, 0]
    for roll in set(DIRAC_ROLLS):
        multiplier = DIRAC_ROLLS.count(roll)
        game = Game(p0=p0, p1=p1, s0=s0, s1=s1, current_turn=turn, winning_score=21)
        game.advance_one_turn(roll)
        if game.scores[0] >= 21:
            win_counts[0] += multiplier
        elif game.scores[1] >= 21:
            win_counts[1] += multiplier
        else:
            counts = get_win_counts(
                s0=game.scores[0],
                s1=game.scores[1],
                p0=game.positions[0],
                p1=game.positions[1],
                turn=game.current_turn,
            )
            win_counts[0] += counts[0] * multiplier
            win_counts[1] += counts[1] * multiplier
    return win_counts


def parse_data(path: str) -> Tuple[int, int]:
    data = read_text_file(path)
    p1, p2 = tuple([int(x.split(":")[1]) for x in data])
    return p1, p2


if __name__ == "__main__":
    p1, p2 = parse_data("data/21.txt")

    ### Part 1
    game = Game(p1, p2)
    game.play()
    print(f"Solution 21a: {min(game.scores) * game.die.n_rolls}")

    ### Part 2
    counts = get_win_counts(p1, p2)
    print(f"Solution 21b: {max(counts)}")
