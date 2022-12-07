import functools

from Day import Day


class Outcome:
    WIN = 6
    DRAW = 3
    LOST = 0
    MAPPING = {"X": LOST, "Y": DRAW, "Z": WIN}


class RPSGame:
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    MAPPING = {
        "A": ROCK,
        "X": ROCK,
        "B": PAPER,
        "Y": PAPER,
        "C": SCISSORS,
        "Z": SCISSORS,
    }
    OUTCOME = {
        ROCK: {ROCK: Outcome.DRAW, PAPER: Outcome.LOST, SCISSORS: Outcome.WIN},
        PAPER: {ROCK: Outcome.WIN, PAPER: Outcome.DRAW, SCISSORS: Outcome.LOST},
        SCISSORS: {ROCK: Outcome.LOST, PAPER: Outcome.WIN, SCISSORS: Outcome.DRAW},
    }

    def __init__(self):
        self.total_point = 0
        self.value_fom_outcome = {}
        self.compute_reverse()

    def round(self, opponent, mine):
        mapped_mine = self.MAPPING[mine]
        mapped_opponent = self.MAPPING[opponent]
        point = mapped_mine
        point += self.OUTCOME[mapped_mine][mapped_opponent]
        self.total_point += point

    def compute_reverse(self):
        for k_mine, v in self.OUTCOME.items():
            for k_opponent, outcome in v.items():
                self.value_fom_outcome[(k_opponent, outcome)] = k_mine

    def round_outcome(self, opponent, outcome):
        mapped_outcome = Outcome.MAPPING[outcome]
        mapped_opponent = self.MAPPING[opponent]
        point = mapped_outcome
        point += self.value_fom_outcome[mapped_opponent, mapped_outcome]
        self.total_point += point


class Day02(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def play_game(game):
        rps = RPSGame()
        for r in game:
            rps.round(r[0], r[2])
        return rps.total_point

    @staticmethod
    def play_game_2(game):
        rps = RPSGame()
        for r in game:
            rps.round_outcome(r[0], r[2])
        return rps.total_point

    def solution_first_star(self, input_value):
        return self.play_game(input_value)

    def solution_second_star(self, input_value):
        return self.play_game_2(input_value)
