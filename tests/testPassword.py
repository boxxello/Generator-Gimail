import unittest

from generator_mail.PasswordGenerator import PasswordGenerator


class TestPassword(unittest.TestCase):
    def main(self):
        self._test_password()

    def _test_password(self):
        passwordGenerator=PasswordGenerator(12,12,True,True,True,True)
        self.assertEqual(len(passwordGenerator._generate_password()),12)
        password=passwordGenerator._generate_password()


if __name__ == '__main__':
    unittest.main()