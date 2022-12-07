import re

from Day import Day


class Day04(Day):
    PATTERN = re.compile(r"\d+")

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def find_overlap(pair):
        nb = 0
        for p in pair:
            r = list(map(int, Day04.pattern.findall(p)))
            if (r[0] <= r[2] and r[3] <= r[1]) or (r[2] <= r[0] and r[1] <= r[3]):
                nb += 1
        return nb

    @staticmethod
    def find_overlap_2(pair):
        nb = 0
        for p in pair:
            r = list(map(int, Day04.PATTERN.findall(p)))
            if (
                r[0] <= r[2] <= r[1]
                or r[0] <= r[3] <= r[1]
                or r[2] <= r[0] <= r[3]
                or r[2] <= r[1] <= r[3]
            ):
                nb += 1
        return nb

    def solution_first_star(self, input_value):
        return self.find_overlap(input_value)

    def solution_second_star(self, input_value):
        return self.find_overlap_2(input_value)
