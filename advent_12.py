from shared import read_text_file
from collections import defaultdict
from typing import List


def parse_data(path: str):
    return read_text_file(path)


class CaveGraph:
    def __init__(self, data: List[str]):
        self.edges = defaultdict(set)
        for line in data:
            cave_1, cave_2 = line.split("-")
            self.add_edge(cave_1, cave_2)

        self.paths = []
        self.paths_2 = []  # allowing one double visit to small cave

    def add_edge(self, node_1: str, node_2: str):
        self.edges[node_1].add(node_2)
        self.edges[node_2].add(node_1)

    def trace_paths(
            self,
            current_node: str = "start",
            current_path: List[str] = None,
    ):
        if current_node == "end":
            self.paths.append(current_path + ["end"])

        else:
            current_path = current_path or []
            current_path = current_path.copy()
            current_path.append(current_node)

            options = [x for x in self.edges[current_node]
                       if x != "start" and (x not in current_path or x != x.lower())]
            for next_node in options:
                self.trace_paths(
                    current_node=next_node,
                    current_path=current_path,
                )

    def trace_paths_2(
            self,
            current_node: str = "start",
            current_path: List[str] = None,
    ):
        """Same as before, but allow a double visit to a single small cave (lowercase)"""
        if current_node == "end":
            self.paths_2.append(current_path + ["end"])

        else:
            current_path = current_path or []
            current_path = current_path.copy()
            current_path.append(current_node)

            made_double_visit = any(current_path.count(x) > 1 for x in current_path
                                    if x == x.lower() and x != "start")
            options = [
                x for x in self.edges[current_node]
                if x != "start" and (x != x.lower() or x not in current_path or not made_double_visit)
            ]
            for next_node in options:
                self.trace_paths_2(
                    current_node=next_node,
                    current_path=current_path,
                )


if __name__ == "__main__":
    data = parse_data("data/12.txt")

    ### Part 1
    graph = CaveGraph(data)
    graph.trace_paths()
    print(f"Solution 12a: {len(graph.paths)}")

    ### Part 2
    graph.trace_paths_2()
    print(f"Solution 12b: {len(graph.paths_2)}")
