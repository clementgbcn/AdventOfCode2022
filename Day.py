import time
from abc import ABC, abstractmethod
from enum import Enum

import DayUtils
from InputParser import InputParser


class Day(ABC):
    def __init__(self, day_inst):
        self.day_value = int(day_inst.__class__.__name__[-2:])

    @abstractmethod
    def solution_first_star(
        self, input_value, input_type=DayUtils.TestEnum.INPUT.value
    ):
        return 0

    @abstractmethod
    def solution_second_star(
        self, input_value, input_type=DayUtils.TestEnum.INPUT.value
    ):
        return 0

    def process_first_star(self):
        self.process_star(DayUtils.Star.FIRST)

    def process_second_star(self):
        self.process_star(DayUtils.Star.SECOND)

    def solution_star(self, star, input_value, input_type):
        if star == DayUtils.Star.FIRST:
            return self.solution_first_star(input_value, input_type=input_type)
        elif star == DayUtils.Star.SECOND:
            return self.solution_second_star(input_value, input_type=input_type)
        else:
            raise DayUtils.UnknownStarException(star)

    def process_star(self, star):
        start_test_time = time.time_ns()
        test_case = InputParser(
            self.day_value, DayUtils.TestEnum.TEST.value, star
        ).get_iterator()
        test_result = self.solution_star(star, test_case, DayUtils.TestEnum.TEST)
        end_test_time = (time.time_ns() - start_test_time) / 1000000
        print(
            f"{self.day_value:>3}\t\t{star}\t\tExample\t\t{test_result:>16}\t|\t{end_test_time:>6}ms"
        )
        start_input_time = time.time_ns()
        input_case = InputParser(
            self.day_value, DayUtils.TestEnum.INPUT.value, star
        ).get_iterator()
        input_result = self.solution_star(star, input_case, DayUtils.TestEnum.INPUT)
        end_input_time = (time.time_ns() - start_input_time) / 1000000
        print(
            f"{self.day_value:>3}\t\t{star}\t\tProblem\t\t{input_result:>16}\t|\t{end_input_time:>6}ms"
        )
