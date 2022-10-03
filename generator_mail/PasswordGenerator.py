import random
import secrets
import string


class PasswordGenerator:
    """
    Generatess strong passwords
    """

    def __init__(self, min_length=12, max_length=12, numbers=True, symbols=True, uppercase=True, lowercase=True):
        self.min_length = min_length
        self.max_length = max_length
        self.numbers = numbers
        self.symbols = symbols
        self.uppercase = uppercase
        self.lowercase = lowercase

    def _generate_n_passwords(self, n) -> list:
        """
        Generates n passwords
        """
        return [self._generate_password() for _ in range(n)]

    def _generate_password(self) -> str:
        """
        Generates a single password
        """
        while True:
            password = "".join(secrets.choice(string.digits + string.ascii_letters + string.punctuation)
                               for _ in range(random.randint(self.min_length, self.max_length)))
            if (any(c.islower() for c in password) and any(c.isupper() for c in password) and
                    any(c.isdigit() for c in password) and any(not c.isalnum() for c in password)):
                break
        return password
