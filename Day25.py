from Day import Day


class SNFU:
    def __init__(self, rpr):
        self.res = 0
        if type(rpr) == str:
            self.str_repr = rpr
            self.from_string(rpr)
        else:
            self.from_int(rpr)

    def from_string(self, str_repr):
        power = 1
        self.res = 0
        for d in str_repr[::-1]:
            if d == "-":
                self.res += -1 * power
            elif d == "=":
                self.res += -2 * power
            else:
                self.res += int(d) * power
            power *= 5

    def from_int(self, int_repr):
        self.res = int_repr
        self.str_repr = ""
        while int_repr > 0:
            remainder = int_repr % 5
            if remainder < 3:
                self.str_repr = str(remainder) + self.str_repr
                int_repr = int_repr // 5
            elif remainder == 3:
                self.str_repr = "=" + self.str_repr
                int_repr = (int_repr + 2) // 5
            else:
                self.str_repr = "-" + self.str_repr
                int_repr = (int_repr + 1) // 5


class Day25(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value):
        res = sum(map(lambda x: SNFU(x).res, input_value))
        return SNFU(res).str_repr

    @staticmethod
    def solve_2(input_value):
        return 0

    def solution_first_star(self, input_value, input_type):
        return self.solve(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
