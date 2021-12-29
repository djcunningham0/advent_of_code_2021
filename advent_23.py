"""
Largely followed the same blueprint from day 15 and implemented Dijkstra's algorithm.
Part 1 runs in about 1.5 seconds, but Part 2 runs takes much longer -- about 12 seconds.
Not entirely sure why it's so much slower (maybe it's some of my lazy code).
"""

from shared import read_text_file
from typing import List, Tuple, Dict, Union, Any
import heapq
from math import inf
from collections import defaultdict


"""
Map:

0  1  2  3  4  5  6  7  8  9  10
     11    12    13    14
     15    16    17    18
(    19    20    21    22       )
(    23    24    25    26       )  additional rows only in part 2


Start (example data, part 1):
A15, A18, B11, B13, C12, C17, D14, D16

End:
A11, A15, B12, B16, C13, C17, D14, D18
"""

DISTANCE_MATRIX: List[List[int]] = [
#     0   1   2  3  4  5  6  7   8   9  10  || 11 12 13  14 |  15  16  17  18  | 19  20  21  22 | 23  24  25  26
    [ 0,  1,  2, 3, 4, 5, 6, 7,  8,  9, 10,     3, 5, 7,  9,    4,  6,  8, 10,    5,  7,  9, 11,   6,  8, 10, 12],  # 0
    [ 1,  0,  1, 2, 3, 4, 5, 6,  7,  8,  9,     2, 4, 6,  8,    3,  5,  7,  9,    4,  6,  8, 10,   5,  7,  9, 11],  # 1
    [ 2,  1,  0, 1, 2, 3, 4, 5,  6,  7,  8,     1, 3, 5,  7,    2,  4,  6,  8,    3,  5,  7,  9,   4,  6,  8, 10],  # 2
    [ 3,  2,  1, 0, 1, 2, 3, 4,  5,  6,  7,     2, 2, 4,  6,    3,  3,  5,  7,    4,  4,  6,  8,   5,  5,  7,  9],  # 3
    [ 4,  3,  2, 1, 0, 1, 2, 3,  4,  5,  6,     3, 1, 3,  5,    4,  2,  4,  6,    5,  3,  5,  7,   6,  4,  6,  8],  # 4
    [ 5,  4,  3, 2, 1, 0, 1, 2,  3,  4,  5,     4, 2, 2,  4,    5,  3,  3,  5,    6,  4,  4,  6,   7,  5,  5,  7],  # 5
    [ 6,  5,  4, 3, 2, 1, 0, 1,  2,  3,  4,     5, 3, 1,  3,    6,  4,  2,  4,    7,  5,  3,  5,   8,  6,  4,  6],  # 6
    [ 7,  6,  5, 4, 3, 2, 1, 0,  1,  2,  3,     6, 4, 2,  2,    7,  5,  3,  3,    8,  6,  4,  4,   9,  7,  5,  5],  # 7
    [ 8,  7,  6, 5, 4, 3, 2, 1,  0,  1,  2,     7, 5, 3,  1,    8,  6,  4,  2,    9,  7,  5,  3,  10,  8,  6,  4],  # 8
    [ 9,  8,  7, 6, 5, 4, 3, 2,  1,  0,  1,     8, 6, 4,  2,    9,  7,  5,  3,   10,  8,  6,  4,  11,  9,  7,  5],  # 9
    [10,  9,  8, 7, 6, 5, 4, 3,  2,  1,  0,     9, 7, 5,  3,   10,  8,  6,  4,   11,  9,  7,  5,  12, 10,  8,  6],  # 10

    [ 3,  2,  1, 2, 3, 4, 5, 6,  7,  8,  9,     0, 4, 6,  8,    1,  5,  7,  9,    2,  6,  8, 10,   3,  7,  9, 11],  # 11
    [ 5,  4,  3, 2, 1, 2, 3, 4,  5,  6,  7,     4, 0, 4,  6,    5,  1,  5,  7,    6,  2,  6,  8,   7,  3,  7,  9],  # 12
    [ 7,  6,  5, 4, 3, 2, 1, 2,  3,  4,  5,     6, 4, 0,  4,    7,  5,  1,  5,    8,  6,  2,  6,   9,  7,  3,  7],  # 13
    [ 9,  8,  7, 6, 5, 4, 3, 2,  1,  2,  3,     8, 6, 4,  0,    9,  7,  5,  1,   10,  8,  6,  2,  11,  9,  7,  3],  # 14

    [ 4,  3,  2, 3, 4, 5, 6, 7,  8,  9, 10,     1, 5, 7,  9,    0,  6,  8, 10,    1,  7,  9, 11,   2,  8, 10, 12],  # 15
    [ 6,  5,  4, 3, 2, 3, 4, 5,  6,  7,  8,     5, 1, 5,  7,    6,  0,  6,  8,    7,  1,  7,  9,   8,  2,  8, 10],  # 16
    [ 8,  7,  6, 5, 4, 3, 2, 3,  4,  5,  6,     7, 5, 1,  5,    8,  6,  0,  6,    9,  7,  1,  7,  10,  8,  2,  8],  # 17
    [10,  9,  8, 7, 6, 5, 4, 3,  2,  3,  4,     9, 7, 5,  1,   10,  8,  6,  0,   11,  9,  7,  1,  12, 10,  8,  2],  # 18

    [ 5,  4,  3, 4, 5, 6, 7, 8,  9, 10, 11,     2, 6, 8, 10,    1,  7,  9, 11,    0,  8, 10, 12,   1,  9, 11, 13],  # 19
    [ 7,  6,  5, 4, 3, 4, 5, 6,  7,  8,  9,     6, 2, 6,  8,    7,  1,  7,  9,    8,  0,  8, 10,   9,  1,  9, 11],  # 20
    [ 9,  8,  7, 6, 5, 4, 3, 4,  5,  6,  7,     8, 6, 2,  6,    9,  7,  1,  7,   10,  8,  0,  8,  11,  9,  1,  9],  # 21
    [11, 10,  9, 8, 7, 6, 5, 4,  3,  4,  5,    10, 8, 6,  2,   11,  9,  7,  1,   12, 10,  8,  0,  13, 11,  9,  1],  # 22

    [ 6,  5,  4, 5, 6, 7, 8, 9, 10, 11, 12,     3, 7, 9, 11,    2,  8, 10, 12,    1,  9, 11, 13,   0, 10, 12, 14],  # 23
    [ 8,  7,  6, 5, 4, 5, 6, 7,  8,  9, 10,     7, 3, 7,  9,    8,  2,  8, 10,    9,  1,  9, 11,  10,  0, 10, 12],  # 24
    [10,  9,  8, 7, 6, 5, 4, 5,  6,  7,  8,     9, 7, 3,  7,   10,  8,  2,  8,   11,  9,  1,  9,  12, 10,  0, 10],  # 25
    [12, 11, 10, 9, 8, 7, 6, 5,  4,  5,  6,    11, 9, 7,  3,   12, 10,  8,  2,   13, 11,  9,  1,  14, 12, 10,  0],  # 26
]

AMPHIPOD_ENERGIES = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

SMALL_DESTINATION = tuple(sorted(("A11", "A15", "B12", "B16", "C13", "C17", "D14", "D18")))
LARGE_DESTINATION = tuple(sorted(("A11", "A15", "A19", "A23",
                                  "B12", "B16", "B20", "B24",
                                  "C13", "C17", "C21", "C25",
                                  "D14", "D18", "D22", "D26")))


class Burrow:
    def __init__(self, starting_state: Tuple[str]):
        self.current_state: Tuple[str] = tuple(sorted(starting_state))
        self.destination = SMALL_DESTINATION
        self.n_slots = 19
        self.home_slots = {
            "A": {11, 15},
            "B": {12, 16},
            "C": {13, 17},
            "D": {14, 18},
        }

        self.distances: Dict[Tuple[str], Union[int, float]] = defaultdict(lambda: inf)
        self.distances[self.current_state] = 0

    def extend(self):
        self.n_slots = 27
        for i, amp in enumerate(self.current_state):
            loc = int(amp[1:])
            if int(amp[1:]) in [15, 16, 17, 18]:
                self.current_state = tuple_replace(self.current_state, i, f"{amp[0]}{loc + 8}")
        self.current_state += ("D15", "C16", "B17", "A18", "D19", "B20", "A21", "C22")
        self.current_state = tuple(sorted(self.current_state))
        self.destination = LARGE_DESTINATION
        self.home_slots = {
            "A": {11, 15, 19, 23},
            "B": {12, 16, 20, 24},
            "C": {13, 17, 21, 25},
            "D": {14, 18, 22, 26},
        }

        self.distances: Dict[Tuple[str], Union[int, float]] = defaultdict(lambda: inf)
        self.distances[self.current_state] = 0

    def dijkstra(self, early_stopping: bool = True) -> Dict[Tuple[str], Union[int, float]]:
        # set up a priority queue that will be sorted by distance
        heap: List[Tuple[int, Tuple[str]]] = []
        heapq.heappush(heap, (0, self.current_state))  # (distance, state)

        # keep track of visited states and known distances to all states
        visited = set()

        while heap:
            # take the first point in the queue, which will be the one with the shortest distance to it
            _, state = heapq.heappop(heap)
            if state in visited:
                continue
            visited.add(state)
            distance = self.distances[state]
            self.current_state = state

            # if we've reached the destination, we're done
            if early_stopping and self.current_state == self.destination:
                return self.distances

            # get the distance to each neighbor -- if it's less than we've seen previously, add it to the queue
            for d, next_state in self.get_possible_next_states():
                next_state = tuple(sorted(next_state))  # order doesn't matter -- sort to avoid duplicate states
                if next_state in visited:
                    continue
                new_distance = distance + d
                if new_distance < self.distances[next_state]:
                    self.distances[next_state] = new_distance
                    heapq.heappush(heap, (new_distance, next_state))

        return self.distances

    def get_possible_next_states(self) -> List[Tuple[int, Tuple[str]]]:
        """Get all possible next states and return list of (distance, state) tuples,
        where state is itself a tuple of strings."""
        occupied = set(int(x[1:]) for x in self.current_state)
        top_occupied = set(x for x in occupied if x < 11)

        # get the well slot that is available to this amphipod
        available_well_slots: Dict[str, Union[int, None]] = dict()
        for t in ["A", "B", "C", "D"]:
            available = None
            for slot in sorted(self.home_slots[t]):
                if slot in occupied:
                    occupant = [x[0] for x in self.current_state if int(x[1:]) == slot][0]
                    if occupant != t:
                        # another type is occupying the well so we can't move in
                        available = None
                        break
                else:
                    available = slot
            available_well_slots[t] = available

        next_states: List[Tuple[int, Tuple[str]]] = []
        for i, amp in enumerate(self.current_state):
            # check if this amphipod is already home and doesn't need to move
            # I didn't feel like generalizing this part, so I wrote these really ugly conditional statements
            skip_conditions = [
                # bottom of its home well
                amp in ["A23", "B24", "C25", "D26"],
                # in well and slot(s) below are occupied by correct type
                amp == "A19" and "A23" in occupied,
                amp == "B20" and "B24" in occupied,
                amp == "C21" and "C25" in occupied,
                amp == "D22" and "D26" in occupied,
                # in well and slots below are occupied, or bottom of the well in small grid
                amp == "A15" and (self.n_slots == 19 or ("A19" in occupied and "A23" in occupied)),
                amp == "B16" and (self.n_slots == 19 or ("B20" in occupied and "B24" in occupied)),
                amp == "C17" and (self.n_slots == 19 or ("C21" in occupied and "C25" in occupied)),
                amp == "D18" and (self.n_slots == 19 or ("D22" in occupied and "D26" in occupied)),
                # in top of well and all slots below are occupied
                amp == "A11" and "A15" in occupied and (self.n_slots == 19 or ("A19" in occupied and "A23" in occupied)),
                amp == "B12" and "B16" in occupied and (self.n_slots == 19 or ("B20" in occupied and "B24" in occupied)),
                amp == "C13" and "C17" in occupied and (self.n_slots == 19 or ("C21" in occupied and "C25" in occupied)),
                amp == "D14" and "D18" in occupied and (self.n_slots == 19 or ("D22" in occupied and "D26" in occupied)),
            ]
            if any(skip_conditions):
                continue

            type_ = amp[0]
            loc = int(amp[1:])
            if loc > 14 and loc - 4 in occupied:
                # blocked by the one above it
                continue

            # assign "virtual" location for the spots above the wells
            if loc < 11:
                virtual_loc = None
            elif loc in [11, 15, 19, 23]:
                virtual_loc = 2
            elif loc in [12, 16, 20, 24]:
                virtual_loc = 4
            elif loc in [13, 17, 21, 25]:
                virtual_loc = 6
            elif loc in [14, 18, 22, 26]:
                virtual_loc = 8
            else:
                raise ValueError(f"Invalid position: {loc}")

            # amphipod can always move into its own well unless it's blocked
            well_slot = available_well_slots[type_]
            if well_slot is not None:
                virtual_well_loc = 2 if type_ == "A" else 4 if type_ == "B" else 6 if type_ == "C" else 8

                blocked = any(between(x, virtual_loc or loc, virtual_well_loc) for x in occupied)
                if not blocked:
                    distance = DISTANCE_MATRIX[loc][well_slot] * AMPHIPOD_ENERGIES[type_]
                    next_state = tuple_replace(self.current_state, i, f"{type_}{well_slot}")
                    next_states.append((distance, next_state))

            # if the amphipod is in a well, it can also move into the top row
            if loc > 10:
                # find the available slots on the top row (can't stop outside a well)
                left_occupied = [x for x in top_occupied if x < virtual_loc] + [-1]  # add -1 in case of empty set
                left_available = [x for x in range(max(left_occupied) + 1, virtual_loc) if x not in [2, 4, 6, 8]]
                right_occupied = [x for x in top_occupied if x > virtual_loc] + [11]  # add 11 in case of empty set
                right_available = [x for x in range(virtual_loc + 1, min(right_occupied)) if x not in [2, 4, 6, 8]]

                for new_loc in left_available + right_available:
                    distance = DISTANCE_MATRIX[loc][new_loc] * AMPHIPOD_ENERGIES[type_]
                    next_state = tuple_replace(self.current_state, i, f"{type_}{new_loc}")
                    next_states.append((distance, next_state))

        return next_states

    def __repr__(self):
        return f"Burrow{self.current_state}"


def between(x, a, b):
    return (a < x < b) or (b < x < a)


def tuple_replace(t: Tuple[Any], index: int, value: Any) -> Tuple:
    return t[:index] + tuple([value]) + t[index + 1:]


def parse_data(path: str) -> Burrow:
    data = read_text_file(path)[2:4]
    loc_list = []
    for i in [0, 1]:
        for j, x in enumerate([3, 5, 7, 9]):
            loc_list.append(f"{data[i][x]}{j+11+i*4}")
    state = tuple(sorted(loc_list))
    return Burrow(state)


if __name__ == "__main__":
    burrow = parse_data("data/23.txt")

    ### Part 1
    d = burrow.dijkstra()
    print(f"Solution 23a: {d[SMALL_DESTINATION]}")

    ### Part 2
    burrow = parse_data("data/23.txt")
    burrow.extend()
    d = burrow.dijkstra()
    print(f"Solution 23b: {d[LARGE_DESTINATION]}")
