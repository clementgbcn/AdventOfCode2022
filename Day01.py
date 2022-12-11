import functools

from Day import Day


class TopList:
    def __init__(self, size):
        self.size = size
        self.top = [0 for _ in range(size)]

    def add(self, value):
        for i in range(self.size):
            if value >= self.top[i]:
                self.top.insert(i, value)
                del self.top[self.size]
                break

    def result(self):
        return functools.reduce(lambda x, y: x + y, self.top)


class Day01(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def count_increment(calories):
        max_calorie = 0
        current_calorie = 0
        for calorie in calories:
            if calorie:
                current_calorie += int(calorie)
            else:
                max_calorie = max(max_calorie, current_calorie)
                current_calorie = 0
        max_calorie = max(max_calorie, current_calorie)
        return max_calorie

    @staticmethod
    def count_increment_2(calories):
        top_list = TopList(3)
        current_calorie = 0
        for calorie in calories:
            if calorie:
                current_calorie += int(calorie)
            else:
                top_list.add(current_calorie)
                current_calorie = 0
        top_list.add(current_calorie)
        return top_list.result()

    def solution_first_star(self, input_value, input_type):
        return self.count_increment(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.count_increment_2(input_value)
