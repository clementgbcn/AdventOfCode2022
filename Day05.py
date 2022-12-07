from Day import Day
from Utils import extract_int


class Day05(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def build_data(lines):
        data = []
        while line := next(lines):
            idx = 0
            while (i := 1 + idx * 4) < len(line):
                if line[i] == "1":
                    break
                if len(data) <= idx:
                    data.append([])
                if line[i] != " ":
                    data[idx].insert(0, line[i])
                idx += 1
        return data

    @staticmethod
    def play_game(lines):
        data = Day05.build_data(lines)
        for line in lines:
            values = extract_int(line)
            for _ in range(values[0]):
                data[values[2] - 1].append(data[values[1] - 1].pop())
        res = "".join(map(lambda x: x.pop(), data))
        return res

    @staticmethod
    def play_game_2(lines):
        data = Day05.build_data(lines)
        for line in lines:
            values = extract_int(line)
            inter = []
            for _ in range(values[0]):
                inter.insert(0, data[values[1] - 1].pop())
            data[values[2] - 1] += inter
        res = "".join(map(lambda x: x.pop(), data))
        return res

    def solution_first_star(self, input_value):
        return self.play_game(input_value)

    def solution_second_star(self, input_value):
        return self.play_game_2(input_value)
