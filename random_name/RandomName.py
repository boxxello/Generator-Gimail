import os

import utils


class RandomNameException(Exception):
    """
    Error: Any of the file we're getting the data from is missing or empty
    """


class UniqueName:

    @staticmethod
    def call_read_names_and_check():
        names = []
        colors = []
        animals = []
        adj = []

        names, colors, animals, adj = UniqueName.read_names_from_data()

        if any([len(names) == 0, len(colors) == 0, len(animals) == 0, len(adj) == 0]):
            raise RandomNameException()

        return names, colors, animals, adj

    @staticmethod
    def read_names_from_data():
        names = []
        colors = []
        animals = []
        adj = []

        with open(os.path.join(utils.Utilities.DATA_DIR_PATH, "names.txt"), "r") as f:
            names.extend(f.read().splitlines())
        with open(os.path.join(utils.Utilities.DATA_DIR_PATH, "colors.txt")) as f:
            colors.extend(f.read().splitlines())
        with open(os.path.join(utils.Utilities.DATA_DIR_PATH, "animals.txt")) as f:
            animals.extend(f.read().splitlines())
        with open(os.path.join(utils.Utilities.DATA_DIR_PATH, "adjectives.txt")) as f:
            adj.extend(f.read().splitlines())

        return names, colors, animals, adj
