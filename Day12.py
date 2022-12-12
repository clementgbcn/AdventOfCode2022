import functools
import sys

from Day import Day


class Cartography:
    def __init__(self, input_value):
        self.height = []
        self.start = (None, None)
        self.end = (None, None)
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
        self.to_visit = [self.end]
        self.minimal_starting = []
        for i in range(len(self.height)):
            for j in range(len(self.height[i])):
                if self.height[i][j] == "a":
                    self.minimal_starting.append((i, j))

    def find_way(self, x, y):
        if (x, y) in self.visited:
            return
        self.visited.add((x, y))
        path = self.shortest_path[x][y]
        height_max = ord(self.height[x][y]) - 1
        if x > 0 and height_max <= ord(self.height[x - 1][y]):
            self.shortest_path[x - 1][y] = min(path + 1, self.shortest_path[x - 1][y])
            self.to_visit.append((x - 1, y))
        if x < len(self.height) - 1 and height_max <= ord(self.height[x + 1][y]):
            self.shortest_path[x + 1][y] = min(path + 1, self.shortest_path[x + 1][y])
            self.to_visit.append((x + 1, y))
        if y > 0 and height_max <= ord(self.height[x][y - 1]):
            self.shortest_path[x][y - 1] = min(path + 1, self.shortest_path[x][y - 1])
            self.to_visit.append((x, y - 1))
        if y < len(self.height[0]) - 1 and height_max <= ord(self.height[x][y + 1]):
            self.shortest_path[x][y + 1] = min(path + 1, self.shortest_path[x][y + 1])
            self.to_visit.append((x, y + 1))

    def visit_graph(self):
        while len(self.to_visit) > 0:
            x, y = self.to_visit.pop(0)
            self.find_way(x, y)

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
