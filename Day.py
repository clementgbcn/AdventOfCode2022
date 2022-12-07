import time
from abc import ABC, abstractmethod
from enum import Enum

from InputParser import InputParser


class Day(ABC):
    class TestEnum(Enum):
        TEST = 0
        INPUT = 1

    class Star(Enum):
        FIRST = 1
        SECOND = 2

        def __str__(self):
            if self.value == Day.Star.FIRST.value:
                return "1st"
            else:
                return "2nd"

    class UnknownStarException(Exception):
        def __init__(self, star):
            super().__init__("Unknown Star: " + star)

    def __init__(self, day_inst):
        self.day_value = int(day_inst.__class__.__name__[-2:])

    @abstractmethod
    def solution_first_star(self, input_value):
        return 0

    @abstractmethod
    def solution_second_star(self, input_value):
        return 0

    def process_first_star(self):
        self.process_star(Day.Star.FIRST)

    def process_second_star(self):
        self.process_star(Day.Star.SECOND)

    def solution_star(self, star, input_value):
        if star == Day.Star.FIRST:
            return self.solution_first_star(input_value)
        elif star == Day.Star.SECOND:
            return self.solution_second_star(input_value)
        else:
            raise Day.UnknownStarException(star)

    def process_star(self, star):
        start_test_time = time.time_ns()
        test_case = InputParser(self.day_value, Day.TestEnum.TEST.value).get_iterator()
        test_result = self.solution_star(star, test_case)
        end_test_time = (time.time_ns() - start_test_time) / 1000000
        print(
            f"{self.day_value:>3}\t\t{star}\t\tExample\t\t{test_result:>16}\t|\t{end_test_time:>6}ms"
        )
        start_input_time = time.time_ns()
        input_case = InputParser(
            self.day_value, Day.TestEnum.INPUT.value
        ).get_iterator()
        input_result = self.solution_star(star, input_case)
        end_input_time = (time.time_ns() - start_input_time) / 1000000
        print(
            f"{self.day_value:>3}\t\t{star}\t\tProblem\t\t{input_result:>16}\t|\t{end_input_time:>6}ms"
        )
