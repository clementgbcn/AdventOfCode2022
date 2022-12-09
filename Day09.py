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
        if abs(knot.x-self.x) > 1:
            self.x += 1 if knot.x > self.x else -1
            if knot.y != self.y:
                self.y += 1 if knot.y > self.y else -1
        elif abs(knot.y-self.y) > 1:
            self.y += 1 if knot.y > self.y else -1
            if knot.x != self.x:
                self.x += 1 if knot.x > self.x else -1


class Rope:

    def __init__(self, nb_knot):
        self.rope = [Knot() for _ in range(nb_knot)]
        self.length = nb_knot
        self.visited_place = {self.rope[-1].get_pos()}

    def move_head(self,direction):
        self.rope[0].move(direction)
        for i in range(1, self.length):
            self.rope[i].get_close(self.rope[i-1])
        self.visited_place.add(self.rope[-1].get_pos())

    def move_rope(self, input_value):
        for order in input_value:
            for _ in range(int(order[2:])):
                self.move_head(order[0])


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

    def solution_first_star(self, input_value):
        return self.solve(input_value)

    def solution_second_star(self, input_value):
        return self.solve_2(input_value)
