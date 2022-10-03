import unittest

from generator_mail.PasswordGenerator import PasswordGenerator
from generator_mail.cli import enable_debug_logging
from generator_mail.logging import get_logger

logger = get_logger()


class TestPassword(unittest.TestCase):

    def test_password(self):
        logger.info("Testing gen passwords")
        passwordGenerator = PasswordGenerator(12, 12, True, True, True, True)
        passw = passwordGenerator._generate_password()
        self.assertIsNotNone(passw)


if __name__ == '__main__':
    enable_debug_logging()
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
