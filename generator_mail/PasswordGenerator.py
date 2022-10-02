

class PasswordGenerator:
    '''
    Generatess strong passwords
    '''

    def __init__(self, min_length=12, max_length=12, numbers=True, symbols=True, uppercase=True, lowercase=True):
        self.min_length = min_length
        self.max_length = max_length
        self.numbers = numbers
        self.symbols = symbols
        self.uppercase = uppercase
        self.lowercase = lowercase



