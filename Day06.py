import itertools

from Day import Day


class Day06(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def get_non_repeated_chain(signal, size):
        computed_set = {}
        nb_distinct = 0
        for i in range(size):
            if (current := computed_set.setdefault(signal[i], 0)) == 0:
                nb_distinct += 1
            computed_set[signal[i]] = current + 1
        starting_idx = 0
        while nb_distinct < size:
            computed_set[signal[starting_idx]] -= 1
            if computed_set[signal[starting_idx]] == 0:
                nb_distinct -= 1
            if (
                current := computed_set.setdefault(signal[starting_idx + size], 0)
            ) == 0:
                nb_distinct += 1
            computed_set[signal[starting_idx + size]] = current + 1
            starting_idx += 1
        return str(starting_idx + size)

    @staticmethod
    def get_non_repeated_chain_suboptimal(signal, size):
        starting_idx = 0
        while len(set(signal[starting_idx : starting_idx + size])) < size:
            starting_idx += 1
        return str(starting_idx + size)

    @staticmethod
    def decrypt_signal(signals):
        return ",".join([Day06.get_non_repeated_chain(signal, 4) for signal in signals])

    @staticmethod
    def decrypt_signal_2(signals):
        return ",".join(
            [Day06.get_non_repeated_chain(signal, 14) for signal in signals]
        )

    def solution_first_star(self, input_value, input_type):
        return self.decrypt_signal(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.decrypt_signal_2(input_value)
