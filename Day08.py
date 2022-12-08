from enum import Enum

from Day import Day


# Day		Star	Test Type	          Result	|	Elapsed Time
#   8		1st		Example		              21	|	  0.15ms
#   8		1st		Problem		            1851	|	42.227ms
#   8		2nd		Example		               8	|	 0.189ms
#   8		2nd		Problem		          574080	|	18.243ms


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class Visibility:
    VISIBLE = 0
    NON_VISIBLE = 1
    NON_VISITED = 2

    def __init__(self):
        self.status = Visibility.NON_VISITED
        self.visible = {direction: False for direction in Direction}


class Forest:

    def __init__(self, input_value):
        self.forest = []
        self.visibility = []
        self.nb_row = 0
        self.nb_col = 0
        self.parse_forest(input_value)

    def parse_forest(self, input_value):
        for row in input_value:
            self.forest.append(list(map(int, [tree for tree in row])))
            self.visibility.append(
                [Visibility() for _ in range(len(row))]
            )
        self.nb_row = len(self.forest)
        self.nb_col = len(self.forest[0])

    def check_directional_visibility(self, directions, direction, x, y, xp, yp, size_check):
        if directions[direction] and size_check and self.forest[x][y] > self.forest[xp][yp]:
            self.check_visibility(xp, yp)
            if (
                    self.visibility[xp][yp].status == Visibility.VISIBLE
                    and self.visibility[xp][yp].visible[direction]
            ):
                self.visibility[x][y].status = Visibility.VISIBLE
                self.visibility[x][y].visible[direction] = True
                directions[direction] = False
        else:
            directions[direction] = False

    def check_visibility(self, x, y):
        if self.visibility[x][y].status != Visibility.NON_VISITED:
            return
        if x == 0 or y == 0 or x == self.nb_row - 1 or y == self.nb_col - 1:
            self.visibility[x][y].status = Visibility.VISIBLE
            self.visibility[x][y].visible[Direction.UP] = x == 0
            self.visibility[x][y].visible[Direction.DOWN] = x == (self.nb_row - 1)
            self.visibility[x][y].visible[Direction.LEFT] = y == 0
            self.visibility[x][y].visible[Direction.RIGHT] = y == (self.nb_col - 1)
            return
        i = 1
        directions = {direction: True for direction in Direction}
        while any(directions.values()):
            self.check_directional_visibility(directions, Direction.UP, x, y, x - i, y, 0 <= x - i)
            self.check_directional_visibility(directions, Direction.DOWN, x, y, x + i, y, x + i < self.nb_row)
            self.check_directional_visibility(directions, Direction.LEFT, x, y, x, y - i, 0 <= y - i)
            self.check_directional_visibility(directions, Direction.RIGHT, x, y, x, y + i, y + i < self.nb_col)
            i += 1
        if self.visibility[x][y].status == Visibility.NON_VISITED:
            self.visibility[x][y].status = Visibility.NON_VISIBLE

    def get_nb_visible_trees(self):
        return sum(
            [
                list(map(lambda x: x.status, row)).count(Visibility.VISIBLE)
                for row in self.visibility
            ]
        )


class Day08(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value):
        forest = Forest(input_value)
        for i in range(forest.nb_row):
            for j in range(forest.nb_col):
                forest.check_visibility(i, j)
        return forest.get_nb_visible_trees()

    @staticmethod
    def solve_2(input_value):
        forest = Forest(input_value).forest
        max_view_dist = 0
        for i in range(1, len(forest) - 1):
            for j in range(1, len(forest[i]) - 1):
                k = 1
                while i - k > 0 and forest[i][j] > forest[i - k][j]:
                    k += 1
                current_view_dist = k
                k = 1
                while i + k < len(forest) - 1 and forest[i][j] > forest[i + k][j]:
                    k += 1
                current_view_dist *= k
                k = 1
                while j - k > 0 and forest[i][j] > forest[i][j - k]:
                    k += 1
                current_view_dist *= k
                k = 1
                while j + k < len(forest[0]) - 1 and forest[i][j] > forest[i][j + k]:
                    k += 1
                current_view_dist *= k
                max_view_dist = max(current_view_dist, max_view_dist)
        return max_view_dist

    def solution_first_star(self, input_value):
        return self.solve(input_value)

    def solution_second_star(self, input_value):
        return self.solve_2(input_value)
