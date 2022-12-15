import sys

import DayUtils
import Utils
from Day import Day

# Day             Star          Test Type                   Result        |       Elapsed Time
#  15             1st             Example                       26        |             0.29ms
#  15             1st             Problem                  4873353        |         1893.602ms
#  15             2nd             Example                 56000011        |            0.261ms
#  15             2nd             Problem           11600823139120        |         32370.56ms
#


class Sensor:
    def __init__(self, input_string):
        parse_input = Utils.extract_int(input_string)
        self.x = parse_input[0]
        self.y = parse_input[1]
        self.bx = parse_input[2]
        self.by = parse_input[3]
        self.dist = abs(self.x - self.bx) + abs(self.y - self.by)

    def cover(self, x, y):
        return abs(self.x - x) + abs(self.y - y) <= self.dist

    def reach(self, row):
        return abs(self.y - row) <= self.dist

    def next_not_cover(self, row):
        return self.dist - abs(self.y - row) + self.x + 1

    def __lt__(self, other):
        if self.x != other.x:
            return self.x < other.x
        return self.y <= other.y


class Tunnel:
    def __init__(self, input_string):
        self.sensors = [Sensor(line) for line in input_string]
        self.sensors.sort()

    def compute_impossible_pos(self, row):
        x_min = sys.maxsize
        x_max = -sys.maxsize
        limited_sensors = []
        beacon_on_row = set()
        for s in self.sensors:
            if s.reach(row):
                limited_sensors.append(s)
                x_min = min(x_min, s.x - s.dist)
                x_max = max(x_max, s.x + s.dist)
                if s.by == row:
                    beacon_on_row.add((s.bx, s.by))
        nb_impossible_location = -len(beacon_on_row)
        starting_index = 0
        x = x_min
        while x <= x_max:
            for i, s in enumerate(limited_sensors[starting_index:]):
                if s.cover(x, row):
                    next_x = s.next_not_cover(row)
                    starting_index += i
                    nb_impossible_location += next_x - x
                    x = next_x
                    break
            else:
                x += 1
        return nb_impossible_location

    def compute_only_pos(self, row):
        for y in range(row):
            x = 0
            limited_sensors = [s for s in self.sensors if s.reach(y)]
            starting_index = 0
            while x < row:
                for i, s in enumerate(limited_sensors[starting_index:]):
                    if s.cover(x, y):
                        x = s.next_not_cover(y)
                        starting_index += i
                        break
                else:
                    return x * 4000000 + y
        return -1


class Day15(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value, input_type):
        tunnel = Tunnel(input_value)
        row = 10 if input_type == DayUtils.TestEnum.TEST else 2000000
        return tunnel.compute_impossible_pos(row)

    @staticmethod
    def solve_2(input_value, input_type):
        tunnel = Tunnel(input_value)
        row = 20 if input_type == DayUtils.TestEnum.TEST else 4000000
        return tunnel.compute_only_pos(row)

    def solution_first_star(self, input_value, input_type):
        return self.solve(input_value, input_type)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value, input_type)
