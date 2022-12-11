import curses

from Day import Day

# Day		Star	Test Type	          Result	|	Elapsed Time
#   9		1st		Example		              13	|	 0.127ms
#   9		1st		Problem		            6498	|	14.689ms
#   9		2nd		Example		              36	|	 0.479ms
#   9		2nd		Problem		            2531	|	 38.57ms


class Knot:
    MOVE_MAP = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}

    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, direction):
        a, b = self.MOVE_MAP[direction]
        self.x += a
        self.y += b

    def get_pos(self):
        return self.x, self.y

    def get_close(self, knot):
        if abs(knot.x - self.x) > 1:
            self.x += 1 if knot.x > self.x else -1
            self.y += 1 if knot.y > self.y else (-1 if knot.y != self.y else 0)
        elif abs(knot.y - self.y) > 1:
            self.y += 1 if knot.y > self.y else -1
            self.x += 1 if knot.x > self.x else (-1 if knot.x != self.x else 0)


class Rope:
    SIZE_ARRAY = 20

    def __init__(self, nb_knot, should_display=False):
        self.rope = [Knot() for _ in range(nb_knot)]
        self.length = nb_knot
        self.visited_place = {self.rope[-1].get_pos()}
        self.should_display = should_display
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

    def move_head(self, direction):
        self.rope[0].move(direction)
        for i in range(1, self.length):
            self.rope[i].get_close(self.rope[i - 1])
        self.display()
        self.visited_place.add(self.rope[-1].get_pos())

    def move_rope(self, input_value):
        list(
            map(
                lambda x: [self.move_head(x[0]) for _ in range(int(x[2:]))], input_value
            )
        )

    def draw_char(self, x, y, char, color=0):
        xp = x + curses.COLS // 2 - 60
        yp = curses.LINES // 2 - y + 130
        if xp < 0 or xp > curses.COLS - 1 or yp < 0 or yp > curses.LINES - 1:
            return
        self.screen.move(yp, xp)
        self.screen.addstr(char, curses.color_pair(color))

    def display(self):
        if not self.should_display:
            return
        self.screen.erase()
        for (x, y) in self.visited_place:
            self.draw_char(x, y, "#")
        for knot in self.rope[1:-1]:
            self.draw_char(knot.x, knot.y, "X", 84)
        self.draw_char(self.rope[-1].x, self.rope[-1].y, "T", 84)
        self.draw_char(self.rope[0].x, self.rope[0].y, "H", 198)
        self.screen.refresh()


class Day09(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value):
        rope = Rope(2)
        rope.move_rope(input_value)
        return len(rope.visited_place)

    @staticmethod
    def solve_2(input_value):
        rope = Rope(10)
        rope.move_rope(input_value)
        return len(rope.visited_place)

    def solution_first_star(self, input_value, input_type):
        return self.solve(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
