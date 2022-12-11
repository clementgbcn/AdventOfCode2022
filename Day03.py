import functools

from Day import Day


class Day03(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def compute_priorities(a):
        return ord(a) - ord("a") + 1 if ord(a) >= ord("a") else ord(a) - ord("A") + 27

    @staticmethod
    def play_game(rucksack):
        return sum(
            map(
                Day03.compute_priorities,
                (
                    set(r[: len(r) // 2]).intersection(set(r[len(r) // 2 :])).pop()
                    for r in rucksack
                ),
            )
        )

    @staticmethod
    def play_game_2(rucksack):
        priorities = 0
        while r := next(rucksack, None):
            current = set(r[:])
            for i in range(0, 2):
                r = next(rucksack)
                current = current.intersection(set(r[:]))
            priorities += Day03.compute_priorities(current.pop())
        return priorities

    def solution_first_star(self, input_value, input_type):
        return self.play_game(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.play_game_2(input_value)
