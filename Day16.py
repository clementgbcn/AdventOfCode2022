import re

import matplotlib.pyplot as plt
import networkx as nx

import DayUtils
import Utils
from Day import Day


class Valve:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.is_open = False

    def open(self):
        self.is_open = True
        return self.rate


class Tunnel:

    VALVE_ID = re.compile("[A-Z]{2}")

    def __init__(self, input_string):
        self.valves = {}
        self.links = {}
        self.nb_with_positive = 0
        for line in input_string:
            valves_id = Tunnel.VALVE_ID.findall(line)
            rate = Utils.extract_int(line)[0]
            if rate > 0:
                self.nb_with_positive += 1
            self.valves[valves_id[0]] = Valve(valves_id[0], rate)
            self.links[valves_id[0]] = {v: 1 for v in valves_id[1:]}
        self.pressure_released = 0
        self.rate = 0
        self.simplify()
        G = nx.Graph()
        for k, v in self.links.items():
            if self.valves[k].rate == 0 and k != "AA":
                continue
            for nxt, dist in v.items():
                G.add_edge(k, nxt, weight=dist)
            print("{}: {}".format(k, v))
        pos = nx.spring_layout(
            G, seed=7
        )  # positions for all nodes - seed for reproducibility
        elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
        # nodes
        nx.draw_networkx_nodes(G, pos, node_size=700)
        # node labels
        nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
        # edge weight labels
        nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels)

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()

    def simplify(self):
        for k, v in self.links.items():
            new_v = {}
            for nxt, dist in v.items():
                if self.valves[nxt].rate == 0:
                    for nxt_nxt, nxt_dist in self.links[nxt].items():
                        if nxt_nxt != k:
                            if nxt_nxt in v and v[nxt_nxt] > dist + nxt_dist:
                                new_v[nxt_nxt] = dist + nxt_dist
                            elif nxt_nxt not in v:
                                new_v[nxt_nxt] = dist + nxt_dist

                else:
                    if nxt not in new_v:
                        new_v[nxt] = dist
            self.links[k] = new_v

    def make_choice(
        self, remaining_time, pressure_released, rate, visited, valve, prev
    ):
        # print("{} - Visiting {} with current pressure {} at a rate of {}".format(remaining_time,valve,pressure_released,rate))
        if remaining_time == 0:
            return pressure_released
        new_pressure = pressure_released + rate
        new_rate = rate
        new_time = remaining_time
        if self.valves[valve].rate > 0 and valve not in visited:
            # It is better to open it
            visited.add(valve)
            new_time -= 1
            new_pressure += rate
            new_rate += self.valves[valve].rate
            if new_time == 0:
                return new_pressure
            if len(visited) == self.nb_with_positive:
                return new_pressure + new_rate * new_time
        maxi = 0
        for next_valve, next_dist in self.links[valve].items():
            if new_time > next_dist:
                new_pressure += next_dist * new_rate
                new_time -= next_dist
            else:
                new_pressure += new_time * rate
                return new_pressure
            maxi = max(
                maxi,
                self.make_choice(
                    new_time, new_pressure, new_rate, visited, next_valve, valve
                ),
            )
        return maxi

    def find_path(self):
        visited = set()
        return self.make_choice(30, 0, 0, visited, "AA", None)


class Day16(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value, input_type):
        tunnel = Tunnel(input_value)
        return tunnel.find_path()

    @staticmethod
    def solve_2(input_value, input_type):
        return 0

    def solution_first_star(self, input_value, input_type):
        return self.solve(input_value, input_type)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value, input_type)
