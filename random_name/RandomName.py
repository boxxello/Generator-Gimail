import os


class RandomNameException(Exception):
    """
    Error: Any of the file we're getting the data from is missing or empty
    """


class UniqueName:
    def __init__(self, data_path:str):
        """
        :param data_path: Path to the data directory
        :param data_path:
        :return:
        """
        self.NAMES, self.COLORS, self.ANIMALS, self.ADJECTIVES = self.call_read_names_and_check(data_path)
        self.LISTS = [self.COLORS, self.ANIMALS, self.ADJECTIVES]

    def call_read_names_and_check(self,data_path: str = None) -> tuple:
        """
        Wrapper fn to read random data from data directory
        :param data_path:
        :return:
        """
        names = []
        colors = []
        animals = []
        adj = []

        names, colors, animals, adj = self.read_names_from_data(data_path)

        if any([len(names) == 0, len(colors) == 0, len(animals) == 0, len(adj) == 0]):
            raise RandomNameException()

        return names, colors, animals, adj


    def read_names_from_data(self,data_path: str ) -> tuple:
        """
        Read random data from data directory
        :param data_path:
        :return:
        """
        names = []
        colors = []
        animals = []
        adj = []

        with open(os.path.join(data_path, "names.txt"), "r") as f:
            names.extend(f.read().splitlines())
        with open(os.path.join(data_path, "colors.txt")) as f:
            colors.extend(f.read().splitlines())
        with open(os.path.join(data_path, "animals.txt")) as f:
            animals.extend(f.read().splitlines())
        with open(os.path.join(data_path, "adjectives.txt")) as f:
            adj.extend(f.read().splitlines())

        return names, colors, animals, adj
