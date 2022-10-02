import random
import secrets
import string

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
    def _generate_n_passwords(self, n):
        '''
        Generates n passwords
        '''
        return [self._generate_password() for _ in range(n)]

    def _generate_password(self):
        '''
        Generates a single password
        '''

        return "".join(secrets.choice(string.digits+string.ascii_letters+string.punctuation) for _ in range(random.randint(self.min_length, self.max_length)))



