from Day import Day

# Day             Star    Test Type                 Result        |       Elapsed Time
#  14             1st             Example                       24        |        0.158ms
#  14             1st             Problem                      805        |       29.218ms
#  14             2nd             Example                       93        |        0.463ms
#  14             2nd             Problem                    25161        |       1299.322ms


class Cave:
    def __init__(self, scans, has_floor=False):
        self.rocks = set()
        self.sand = set()
        self.x_start, self.y_start = 500, 0
        self.bottom = 0
        self.has_floor = has_floor
        for scan in scans:
            checkpoints = scan.split(" -> ")
            xp, yp = None, None
            for checkpoint in checkpoints:
                [x, y] = list(map(int, checkpoint.split(",")))
                if xp is None:
                    self.rocks.add((x, y))
                else:
                    for x_var in range(min(xp, x), max(xp, x) + 1):
                        for y_var in range(min(yp, y), max(yp, y) + 1):
                            self.rocks.add((x_var, y_var))
                xp, yp = x, y
                self.bottom = max(self.bottom, y)

    def produce_one_unit_of_sand(self):
        x, y = self.x_start, self.y_start
        while y <= self.bottom or self.has_floor:
            x_next, y_next = self.find_next_position(x, y)
            if x_next == x and y_next == y:
                self.sand.add((x, y))
                return x_next != self.x_start or y_next != self.y_start
            x, y = x_next, y_next
        return False

    def produce_sand(self):
        while self.produce_one_unit_of_sand():
            continue
        return len(self.sand)

    def find_next_position(self, x, y):
        if self.has_floor and y + 1 == self.bottom + 2:
            return x, y
        for i in [0, -1, 1]:
            if (x + i, y + 1) not in self.rocks and (x + i, y + 1) not in self.sand:
                return x + i, y + 1
        return x, y


class Day14(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value):
        cave = Cave(input_value)
        return cave.produce_sand()

    @staticmethod
    def solve_2(input_value):
        cave = Cave(input_value, has_floor=True)
        return cave.produce_sand()

    def solution_first_star(self, input_value, input_type):
        return self.solve(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
