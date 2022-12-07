import os


class InputParser:

    FOLDER = "inputs/"

    def __init__(self, day, star):
        self.day = day
        self.star = star
        self.filename = None
        self.filepath = None
        self.build_file_path()

    def build_file_path(self):
        self.filename = "{0}-{1}.txt".format(self.day, self.star)
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
