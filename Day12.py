import functools
import sys

from Day import Day


class Cartography:
    def __init__(self, input_value):
        self.height = []
        self.shortest_path = []
        for row_idx, row in enumerate(input_value):
            row_copy = list(row)
            if "S" in row:
                s_index = row.index("S")
                self.start = (row_idx, s_index)
                row_copy[s_index] = "a"
            if "E" in row:
                e_index = row.index("E")
                self.end = (row_idx, e_index)
                row_copy[e_index] = "z"
            self.height.append(row_copy)
            self.shortest_path.append([sys.maxsize for _ in range(len(row_copy))])
        self.shortest_path[self.end[0]][self.end[1]] = 0
        self.visited = set()
        self.to_visit = [(self.end[0], self.end[1], 0)]
        self.minimal_starting = []
        for i in range(len(self.height)):
            self.minimal_starting += [
                (i, j) for j in range(len(self.height[i])) if self.height[i][j] == "a"
            ]

    def find_way_and_update(self, x, y, path):
        self.shortest_path[x][y] = min(path + 1, self.shortest_path[x][y])
        if (x, y) in self.visited:
            return
        self.visited.add((x, y))
        path = self.shortest_path[x][y]
        height_max = ord(self.height[x][y]) - 1
        for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (i != 0 and 0 <= x + i < len(self.height)) or (
                j != 0 and 0 <= (y + j) < len(self.height[0])
            ):
                if height_max <= ord(self.height[x + i][y + j]):
                    self.to_visit.append((x + i, y + j, path))

    def visit_graph(self):
        while len(self.to_visit) > 0:
            x, y, path = self.to_visit.pop(0)
            self.find_way_and_update(x, y, path)

    def find_way_from_end(self):
        self.visit_graph()
        return self.shortest_path[self.start[0]][self.start[1]]

    def find_minimal_start(self):
        self.visit_graph()
        return min(map(lambda p: self.shortest_path[p[0]][p[1]], self.minimal_starting))


class Day12(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value):
        c = Cartography(input_value)
        return c.find_way_from_end()

    @staticmethod
    def solve_2(input_value):
        c = Cartography(input_value)
        return c.find_minimal_start()

    def solution_first_star(self, input_value, input_type):
        return self.solve(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
