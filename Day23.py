import sys
from enum import Enum

from Day import Day

# Day		Star	Test Type	          Result	|	Elapsed Time
#  23		1st		Example		             110	|	 0.676ms
#  23		1st		Problem		            4045	|	75.113ms
#  23		2nd		Example		              20	|	 0.921ms
#  23		2nd		Problem		             963	|	5261.284ms


class Direction(Enum):

    N = (
        -1,
        0,
    )
    S = (
        1,
        0,
    )
    W = 0, -1
    E = 0, 1


class Grid:
    def __init__(self, input_values):
        self.elves = set()
        self.max_x = 0
        self.min_x = sys.maxsize
        self.max_y = 0
        self.min_y = sys.maxsize
        i = 0
        for line in input_values:
            for j, elt in enumerate(line[:]):
                if elt == "#":
                    self.elves.add((i, j))
            i += 1
        self.nb_round = 0

    def update_extrema(self):
        for x, y in self.elves:
            self.max_x = max(self.max_x, x)
            self.min_x = min(self.min_x, x)
            self.max_y = max(self.max_y, y)
            self.min_y = min(self.min_y, y)

    def compute_progress(self):
        self.update_extrema()
        return (self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1) - len(
            self.elves
        )

    def move(self, x, y, new_set):
        moves = self.get_moves()
        for i in range(4):
            if moves[(self.nb_round + i) % 4](x, y, new_set):
                return

    def get_moves(self):
        return [
            self.try_move_north,
            self.try_move_south,
            self.try_move_west,
            self.try_move_east,
        ]

    def try_move_dir(self, direction, x, y, new_set):
        dir_x, dir_y = direction.value
        mul_x = 1 if dir_x == 0 else 0
        mul_y = 1 if dir_y == 0 else 0
        xp = x + dir_x
        yp = y + dir_y
        for i in [-1, 0, 1]:
            if (xp + mul_x * i, yp + mul_y * i) in self.elves:
                return False
        new_set.setdefault((xp, yp), set()).add((x, y))
        return True

    def try_move_north(self, x, y, new_set):
        return self.try_move_dir(Direction.N, x, y, new_set)

    def try_move_south(self, x, y, new_set):
        return self.try_move_dir(Direction.S, x, y, new_set)

    def try_move_west(self, x, y, new_set):
        return self.try_move_dir(Direction.W, x, y, new_set)

    def try_move_east(self, x, y, new_set):
        return self.try_move_dir(Direction.E, x, y, new_set)

    def do_round(self):
        new_set = dict()
        for x, y in self.elves:
            found = False
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue
                    if (x + i, y + j) in self.elves:
                        found = True
                        break
                if found:
                    break
            if found:
                self.move(x, y, new_set)
            else:
                # Find Nothing do not move
                new_set[(x, y)] = new_set.get((x, y), set())
                new_set[(x, y)].add((x, y))
        # Let process the dict
        moved = False
        for k, v in new_set.items():
            if len(v) == 1:
                new_elf = v.pop()
                if new_elf != k:
                    moved = True
                    self.elves.add(k)
                    self.elves.remove(new_elf)
        self.nb_round += 1
        return moved

    def do_rounds(self, n):
        for r in range(n):
            self.do_round()
        return self.compute_progress()

    def find_stability(self):
        while self.do_round():
            continue
        return self.nb_round


class Day23(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value):
        grid = Grid(input_value)
        return grid.do_rounds(10)

    @staticmethod
    def solve_2(input_value):
        grid = Grid(input_value)
        return grid.find_stability()

    def solution_first_star(self, input_value, input_type):
        return self.solve(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
