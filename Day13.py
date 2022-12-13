import bisect

from Day import Day

# Day             Star    Test Type                 Result        |       Elapsed Time
#  13             1st             Example                        8        |        0.105ms
#  13             1st             Problem                     5330        |        3.385ms
#  13             2nd             Example                      180        |        0.144ms
#  13             2nd             Problem                    27648        |        6.624ms


class Packet:
    def __init__(self, input_str):
        self.data = self.parse_string(input_str)

    def __lt__(self, other):
        return self.compare_pair(self.data, other.data)

    @staticmethod
    def parse_string(input_str):
        stack = []
        current_list = []
        current_number = ""
        for i in input_str[1:-1]:
            if i == "[":
                stack.append(current_list)
                current_list = []
            elif i == "]":
                if current_number != "":
                    current_list.append(int(current_number))
                    current_number = ""
                previous = stack.pop()
                previous.append(current_list)
                current_list = previous
            elif ord("0") <= ord(i) <= ord("9"):
                current_number += i
            elif current_number != "":
                current_list.append(int(current_number))
                current_number = ""
        return current_list

    @staticmethod
    def compare_pair(left, right):
        i = 0
        while i < min(len(left), len(right)):
            res = None
            is_left_list = type(left[i]) == list
            is_right_list = type(right[i]) == list
            if not is_left_list and not is_right_list:
                if left[i] != right[i]:
                    return left[i] < right[i]
            else:
                res = Packet.compare_pair(
                    left[i] if is_left_list else [left[i]],
                    right[i] if is_right_list else [right[i]],
                )
            if res is not None:
                return res
            i += 1
        return None if len(left) == len(right) else len(left) < len(right)


class Day13(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value):
        idx = 1
        result = 0
        while pair := next(input_value, None):
            first = Packet(pair)
            second = Packet(next(input_value))
            if first < second:
                result += idx
            idx += 1
            next(input_value, None)
        return result

    @staticmethod
    def solve_2(input_value):
        packets = []
        while pair := next(input_value, None):
            bisect.insort(packets, Packet(pair))
            bisect.insort(packets, Packet(next(input_value)))
            next(input_value, None)
        return (bisect.bisect(packets, Packet("[[2]]")) + 1) * (
            bisect.bisect(packets, Packet("[[6]]")) + 2
        )

    def solution_first_star(self, input_value, input_type):
        return self.solve(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
