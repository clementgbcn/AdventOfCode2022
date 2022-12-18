import sys

from Day import Day


class Grid:
    def __init__(self, input_value):
        self.grid = {}
        self.nb_face = 0
        self.maxi = [-sys.maxsize for _ in range(3)]
        self.mini = [sys.maxsize for _ in range(3)]
        for cube in input_value:
            add_face = 6
            pos = list(map(int, cube.split(",")))
            orientation = set()
            for i in range(3):
                for k in [-1, 1]:
                    side = tuple([pos[idx] + k * (idx == i) for idx in range(3)])
                    presence = side in self.grid
                    way = -1 if presence else 1
                    side_or = tuple([way * k * (idx == i) for idx in range(3)])
                    if presence:
                        add_face -= 2
                        self.grid[side].remove(side_or)
                    else:
                        orientation.add(side_or)
            self.nb_face += add_face
            for i in range(3):
                self.maxi[i] = max(self.maxi[i], pos[i])
                self.mini[i] = min(self.mini[i], pos[i])
            self.grid[(pos[0], pos[1], pos[2])] = orientation

    def compute_internal(self):
        all_visited = set()
        nb_to_remove = 0
        for cube, o in self.grid.items():
            if len(o) == 0:
                continue
            for n in o:
                nxt_pos = tuple([cube[idx] + n[idx] for idx in range(3)])
                if nxt_pos in all_visited:
                    continue
                stack = [nxt_pos]
                visited = set()
                to_remove = 0
                while len(stack) > 0:
                    nxt = stack.pop()
                    if nxt in visited:
                        continue
                    visited.add(nxt)
                    if not all(
                        [
                            self.mini[idx] <= nxt[idx] <= self.maxi[idx]
                            for idx in range(3)
                        ]
                    ):
                        break
                    for i in range(3):
                        for k in [-1, 1]:
                            nxt_to_visit = tuple(
                                [nxt[idx] + (idx == i) * k for idx in range(3)]
                            )
                            if nxt_to_visit not in self.grid:
                                stack.append(nxt_to_visit)
                            else:
                                to_remove += 1
                else:
                    all_visited.update(visited)
                    nb_to_remove += to_remove
        return self.nb_face - nb_to_remove


class Day18(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value):
        grid = Grid(input_value)
        return grid.nb_face

    @staticmethod
    def solve_2(input_value):
        grid = Grid(input_value)
        return grid.compute_internal()

    def solution_first_star(self, input_value, input_type):
        return self.solve(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
