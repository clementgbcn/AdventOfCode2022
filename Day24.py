from Day import Day


class Valley:
    def __init__(self, input_blizzard):
        self.pos = (0, 0)
        self.blizzard = {}
        i = 1
        first_line = next(input_blizzard)
        self.max_y = len(first_line) - 1
        for line in input_blizzard:
            for j, c in enumerate(line[::]):
                if c != "#" and c != ".":
                    self.blizzard[(i, j)] = [c]
            i += 1
        self.max_x = i - 1
        self.steps = 0

    def move_blizzard(self):
        new_blizzard = {}
        for pos, ways in self.blizzard.items():
            x, y = pos
            for way in ways:
                if way == "<":
                    new_pos = (x, self.max_y - 1 if y == 1 else y - 1)
                elif way == ">":
                    new_pos = (x, 1 if y == self.max_y - 1 else y + 1)
                elif way == "^":
                    new_pos = (self.max_x - 1 if x == 1 else x - 1, y)
                elif way == "v":
                    new_pos = (1 if x == self.max_x - 1 else x + 1, y)
                new_blizzard.setdefault(new_pos, []).append(way)
        self.blizzard = new_blizzard
        self.steps += 1

    def find_path(self, start, end):
        current_pos = [start]
        while True:
            self.move_blizzard()
            new_pos = set()
            for pos in current_pos:
                if pos == end:
                    return self.steps
                if pos not in self.blizzard:
                    new_pos.add(pos)
                x, y = pos
                if x > 1 and (x - 1, y) not in self.blizzard:
                    new_pos.add((x - 1, y))
                if x < self.max_x - 1 and (x + 1, y) not in self.blizzard:
                    new_pos.add((x + 1, y))
                if (
                    x > 0
                    and x < self.max_x
                    and y > 1
                    and (x, y - 1) not in self.blizzard
                ):
                    new_pos.add((x, y - 1))
                if (
                    x > 0
                    and x < self.max_x
                    and y < self.max_y - 1
                    and (x, y + 1) not in self.blizzard
                ):
                    new_pos.add((x, y + 1))
            current_pos = new_pos


class Day24(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value):
        valley = Valley(input_value)
        return valley.find_path((0, 1), (valley.max_x - 1, valley.max_y - 1))

    @staticmethod
    def solve_2(input_value):
        valley = Valley(input_value)
        valley.find_path((0, 1), (valley.max_x - 1, valley.max_y - 1))
        valley.find_path((valley.max_x, valley.max_y - 1), (1, 1))
        return valley.find_path((0, 1), (valley.max_x - 1, valley.max_y - 1))

    def solution_first_star(self, input_value, input_type):
        return self.solve(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
