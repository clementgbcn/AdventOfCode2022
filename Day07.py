import functools
import re

from Day import Day


class Graph:
    PATTERN_CD = re.compile(r"^\$\ cd\ (.*)")
    PATTERN_LS_FILE = re.compile(r"(\d+)\ (.*)")
    PATTERN_LS_DIR = re.compile(r"dir (.*)")
    CMD_START = "$"
    CMD_CD_PARENT = CMD_START + " cd .."
    CMD_LS = CMD_START + " ls"
    THRESHOLD_DELETION = 40000000

    def __init__(self, input_value):
        self.root_node = Node("/", True, 0, None)
        self.build_graph(input_value)

    def build_graph(self, input_value):
        current_node_dir = None
        data = next(input_value)
        while data:
            if data == Graph.CMD_CD_PARENT:
                # Update the size
                current_node_dir.size = sum(
                    [child.size for child in current_node_dir.children.values()]
                )
                current_node_dir = current_node_dir.parent
            elif data == Graph.CMD_LS:
                while (data := next(input_value, None)) and data[0] != Graph.CMD_START:
                    directory = Graph.PATTERN_LS_DIR.findall(data)
                    if len(directory) > 0:
                        current_node_dir.children[directory[0]] = Node(
                            directory[0], True, 0, current_node_dir
                        )
                        continue
                    file = Graph.PATTERN_LS_FILE.findall(data).pop()
                    current_node_dir.children[file[1]] = Node(
                        file[1], False, int(file[0]), current_node_dir
                    )
                continue
            elif current_node_dir:
                cmd = Graph.PATTERN_CD.findall(data).pop()
                current_node_dir = current_node_dir.children[cmd]
            else:
                current_node_dir = self.root_node
            data = next(input_value)
        while current_node_dir.parent:
            current_node_dir.size = sum(
                [child.size for child in current_node_dir.children.values()]
            )
            current_node_dir = current_node_dir.parent
        current_node_dir.size = sum(
            [child.size for child in current_node_dir.children.values()]
        )

    def sum_small_dir(self):
        return self.root_node.sum_small_dir()

    def find_smallest_folder_to_delete(self):
        return self.root_node.just_above_threshold(
            self.root_node.size - Graph.THRESHOLD_DELETION
        )


class Node:
    DIR_THRESHOLD = 100000

    def __init__(self, name, is_dir, size, parent):
        self.name = name
        self.is_dir = is_dir
        self.children = {}
        self.size = size
        self.parent = parent

    def sum_small_dir(self):
        res = sum([child.sum_small_dir() for child in self.children.values()])
        if self.size < self.DIR_THRESHOLD and self.is_dir and self.parent:
            res += self.size
        return res

    def just_above_threshold(self, threshold):
        current_min = None
        for child in self.children.values():
            res = child.just_above_threshold(threshold)
            if res is not None:
                current_min = min(res, current_min) if current_min is not None else res
        if self.size > threshold and self.is_dir and self.parent:
            current_min = (
                min(self.size, current_min) if current_min is not None else self.size
            )
        return current_min


class Day07(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value):
        graph = Graph(input_value)
        return graph.sum_small_dir()

    @staticmethod
    def solve_2(input_value):
        graph = Graph(input_value)
        return graph.find_smallest_folder_to_delete()

    def solution_first_star(self, input_value):
        return self.solve(input_value)

    def solution_second_star(self, input_value):
        return self.solve_2(input_value)
