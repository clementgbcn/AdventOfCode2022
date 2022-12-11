import curses
import functools
from time import sleep

import Utils
from Day import Day

# Day             Star    Test Type                         Result        |       Elapsed Time
#  11             1st             Example                    10605        |            0.462ms
#  11             1st             Problem                   102399        |             1.13ms
#  11             2nd             Example               2713310158        |           95.965ms
#  11             2nd             Problem              23641658401        |          437.096ms
#
# Process finished with exit code 0


class Monkey:
    def __init__(self, input_value, worry_decrease, idx):
        line = next(input_value)
        self.objects = Utils.extract_int(line)
        line = next(input_value)
        self.ope = int.__mul__ if line[23] == "*" else int.__add__
        self.ope_value = None if line[25:] == "old" else int(line[25:])
        line = next(input_value)
        self.divisibility = int(line[21:])
        line = next(input_value)
        self.if_true = int(line[29:])
        line = next(input_value)
        self.if_false = int(line[30:])
        self.nb_object = 0
        self.worry_decrease = worry_decrease
        self.idx = idx
        next(input_value, None)

    def do_a_turn(self, monkey_lists, remainder, display_method=None):
        while len(self.objects) > 0:
            self.nb_object += 1
            if display_method:
                display_method(self.idx, None, False)
            worry = self.objects.pop(0)
            worry = self.ope(worry, self.ope_value if self.ope_value else worry)
            worry = (
                (worry // self.worry_decrease)
                if self.worry_decrease
                else worry % remainder
            )
            next_monkey = (
                self.if_true if worry % self.divisibility == 0 else self.if_false
            )
            monkey_lists[next_monkey].objects.append(worry)
            if display_method:
                display_method(self.idx, next_monkey, True)


class Rounds:
    def __init__(self, input_value, worry_decrease, should_display=False):
        self.monkeys = []
        idx = 0
        while next(input_value, None):
            self.monkeys.append(Monkey(input_value, worry_decrease, idx))
            idx += 1
        self.remainder = functools.reduce(
            int.__mul__, [m.divisibility for m in self.monkeys]
        )
        self.should_display = should_display
        self.current_round = 0
        if self.should_display:
            self.screen = curses.initscr()
            curses.noecho()
            curses.cbreak()
            curses.start_color()
            curses.use_default_colors()
            for i in range(0, curses.COLORS):
                curses.init_pair(i + 1, i, -1)
            self.screen.keypad(True)
            self.screen.idcok(False)

    def do_a_round(self):
        self.current_round += 1
        for monkey in self.monkeys:
            monkey.do_a_turn(self.monkeys, self.remainder, self.display_monkey)

    def get_max(self):
        max1, max2 = 0, 0
        for monkey in self.monkeys:
            if monkey.nb_object > max1:
                max1, max2 = monkey.nb_object, max1
            elif monkey.nb_object > max2:
                max2 = monkey.nb_object
        return max1 * max2

    def display_monkey(self, idx, idx_dest, after=False):
        if not self.should_display:
            return
        self.screen.erase()
        self.screen.addstr("\n")
        self.screen.addstr("\tROUND {}".format(self.current_round))
        self.screen.addstr("\n\n")
        for i, m in enumerate(self.monkeys):
            self.screen.addstr("\t")
            if i == idx:
                self.screen.addstr(
                    "Monkey {}: ".format(i, m.nb_object), curses.color_pair(198)
                )
                self.screen.addstr("{{{:3d}}} ".format(m.nb_object))
                list_str = str(m.objects)
                if after:
                    self.screen.addstr(list_str)
                else:
                    comma = (
                        list_str.index(",") if "," in list_str else len(list_str) - 1
                    )
                    self.screen.addstr(list_str[0])
                    self.screen.addstr(list_str[1:comma], curses.color_pair(40))
                    self.screen.addstr(list_str[comma:])
            elif i == idx_dest and after:
                self.screen.addstr("Monkey {}: {{{:3d}}} ".format(i, m.nb_object))
                list_str = str(m.objects)
                comma = list_str.rindex(",") if "," in list_str else 0
                self.screen.addstr(list_str[0 : comma + 1])
                self.screen.addstr(list_str[comma + 1 : -1], curses.color_pair(119))
                self.screen.addstr(list_str[-1])
            else:
                self.screen.addstr(
                    "Monkey {}: {{{:3d}}} {}".format(i, m.nb_object, str(m.objects))
                )
            self.screen.addstr("\n")
        self.screen.refresh()
        sleep(0.04)


class Day11(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value, input_type):
        rounds = Rounds(input_value, 3)
        for _ in range(20):
            rounds.do_a_round()
        return rounds.get_max()

    @staticmethod
    def solve_2(input_value):
        rounds = Rounds(input_value, None)
        for _ in range(10000):
            rounds.do_a_round()
        return rounds.get_max()

    def solution_first_star(self, input_value, input_type):
        return self.solve(input_value, input_type)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
