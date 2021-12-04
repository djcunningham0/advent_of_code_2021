from shared import read_text_file
from typing import List, Tuple


MARKED_NUMBERS = {i: False for i in range(100)}


def mark_number(x: int):
    MARKED_NUMBERS[x] = True


def is_marked(x: int):
    return MARKED_NUMBERS[x]


def reset_marked_numbers():
    for i in MARKED_NUMBERS:
        MARKED_NUMBERS[i] = False


class Board:
    def __init__(self, board_data: List[str]):
        self.n = len(board_data)
        self.rows = [parse_single_line_to_numbers(x) for x in board_data]
        self.columns = [[self.rows[i][j] for i in range(self.n)] for j in range(self.n)]

    def row_is_complete(self, row_index) -> bool:
        return all(is_marked(x) for x in self.rows[row_index])

    def column_is_complete(self, column_index) -> bool:
        return all(is_marked(x) for x in self.columns[column_index])

    def any_rows_complete(self) -> bool:
        return any(self.row_is_complete(i) for i in range(self.n))

    def any_columns_complete(self) -> bool:
        return any(self.column_is_complete(j) for j in range(self.n))

    def board_is_complete(self):
        return self.any_rows_complete() or self.any_columns_complete()

    def get_unmarked_numbers(self):
        all_numbers_on_board = [x for y in self.rows for x in y]
        return [x for x in all_numbers_on_board if not is_marked(x)]


def parse_single_line_to_numbers(line: str) -> List[int]:
    """e.g., "10 15  6 25 90" --> [10, 15, 6, 25, 90]"""
    return [int(line[i:i+2]) for i in range(0, len(line), 3)]


def parse_order_and_boards(data: List[str]) -> Tuple[List[int], List[Board]]:
    """Parse the order and boards from the input data"""
    reset_marked_numbers()
    order = [int(x) for x in data[0].split(",")]
    boards = []
    for i in range(2, len(data), 6):
        board = Board(data[i:i + 5])
        boards.append(board)
    return order, boards


def find_winning_board(order: List[int], boards: List[Board]) -> Tuple[Board, int]:
    """
    Given the ordered list of numbers to be marked and the list of boards, return the
    winning board and how many numbers were called to find the winner.
    """
    # first four numbers can't result in a winner
    [mark_number(x) for x in order[:4]]

    # mark numbers one at a time and stop when we have a winner
    for i, x in enumerate(order[4:]):
        mark_number(x)
        statuses = [x.board_is_complete() for x in boards]
        if any(statuses):
            winner = boards[statuses.index(True)]  # return the first winner
            return winner, i + 4  # +4 because we processed the first four separately

    raise(ValueError("No winners found"))  # should never reach this point


def find_losing_board(order: List[int], boards: List[Board]) -> Tuple[Board, int]:
    """Return the last board to win and the index of the last number marked on the board."""
    # first four numbers can't result in a winner
    [mark_number(x) for x in order[:4]]

    # mark numbers one at a time
    for i, x in enumerate(order[4:]):
        mark_number(x)
        if len(boards) > 1:
            # there are more boards remaining -- throw out the winners
            boards = [x for x in boards if not x.board_is_complete()]
        else:
            # there is only one remaining board -- check if it's won yet
            board = boards[0]
            if board.board_is_complete():
                return board, i + 4  # +4 because we processed the first four separately

    raise (ValueError("At least one board never wins"))  # should never reach this point


def calculate_board_score(board: Board, last_number: int) -> int:
    """Sum of all unmarked numbers times the last marked number."""
    return sum(board.get_unmarked_numbers() * last_number)


if __name__ == "__main__":
    data = read_text_file("data/04.txt", dtype=str)
    order, boards = parse_order_and_boards(data)

    ### Part 1
    winner, n = find_winning_board(order, boards)
    solution = calculate_board_score(winner, order[n])
    print(f"solution 04a: {solution}")

    ### Part 2
    loser, n = find_losing_board(order, boards)
    solution = calculate_board_score(loser, order[n])
    print(f"solution 04b: {solution}")
