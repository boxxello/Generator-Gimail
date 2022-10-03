class RandomNameException(Exception):
    """
    Error: Any of the file we're getting the data from is missing or empty
    """



class UniqueName:


    @staticmethod
    def call_read_names_and_check():
        names=[]
        colors=[]
        animals=[]
        adj=[]
        names, colors, animals, adj = UniqueName.read_names_from_data()
        if any([len(names)==0, len(colors)==0, len(animals)==0, len(adj)==0]):
            raise RandomNameException()
        return names, colors, animals, adj

    @staticmethod
    def read_names_from_data():
        names=[]
        colors=[]
        animals=[]
        adj=[]

        with open("data/names.txt", "r") as f:
            names.append(f.read().splitlines())
        with open("data/colors.txt", "r") as f:
            colors.append( f.read().splitlines())
        with open("data/animals.txt", "r") as f:
           animals.append(f.read().splitlines())
        with open("data/adjectives.txt", "r") as f:
            adj.append( f.read().splitlines())
        return names, colors, animals, adj



