import os

import DayUtils


class InputParser:

    FOLDER = "inputs/"

    def __init__(self, day, input_type, star):
        self.day = day
        self.input_type = input_type
        self.star = star
        self.filename = None
        self.filepath = None
        self.build_file_path()

    def build_file_path(self):
        if self.star == DayUtils.Star.SECOND and self.input_type == DayUtils.TestEnum.TEST.value:
            self.filename = "{0}-{1}-{2}.txt".format(self.day, self.input_type, self.star.value)
            self.filepath = os.path.join(InputParser.FOLDER, self.filename)
            if os.path.exists(self.filepath):
                return
        self.filename = "{0}-{1}.txt".format(self.day, self.input_type)
        self.filepath = os.path.join(InputParser.FOLDER, self.filename)

    def get_iterator(self):
        with open(self.filepath, "r") as f:
            for line in f:
                yield line[:-1]

    def get_table(self):
        res = []
        with open(self.filepath, "r") as f:
            for line in f:
                res.append(line[:-1])
        return res
