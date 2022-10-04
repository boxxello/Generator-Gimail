import os
from typing import Tuple

from cli.DriverManager import ALL_VALID_BROWSER_STRINGS
from utils.utils import Utilities
from utils.logging import get_logger

logger = get_logger()


class Settings:
    def __init__(self, browser, min_length, max_length, numbers, symbols, uppercase, lowercase, settings_file_path: str = "settings.yaml"):
        # set_browser returns a Tuple[str, bool] where str = browser and parameter and bool = True if browser
        # should be saved as default.
        # The same logic is applied to all "_set_x" methods
        self.browser, self.save_browser = self._set_browser(browser)
        self.min_length, self.save_min_length = self._set_min_length(min_length)
        self.max_length, self.save_max_length = self._set_min_length(max_length)
        self.numbers, self.save_numbers = self._set_numbers(numbers)
        self.symbols, self.save_symbols = self._set_symbols(symbols)
        self.uppercase, self.save_uppercase = self._set_uppercase(uppercase)
        self.lowercase, self.save_lowercase = self._set_lowercase(lowercase)

        self.should_store_parameters = False
        self._settings_file_path = os.join((Utilities.get_app_dir(), settings_file_path))

    def _init_settings(self) -> None:
        """
           Initialize the settings to be used in the script

           :return:
        """

        settings = self._load_user_settings()
        if settings is None:
            self._generate_settings()
            self._save_settings()

    def _set_browser(self, browser) -> Tuple[str, bool]:

        if len(browser) == 0 or browser not in ALL_VALID_BROWSER_STRINGS or browser:
            logger.warning(f"Invalid browser: {browser}")
            logger.info(f"Valid browsers: {ALL_VALID_BROWSER_STRINGS}")
            return self._set_browser(input("Please enter a valid browser: "))

        save = input(f"Save {browser} as default browser? (y/n): ")

        return browser, save.lower()[0] == "y"

    def _set_min_length(self, min_length) -> Tuple[int, bool]:

        if min_length:
            try:
                min_length = int(min_length)
            except ValueError:
                logger.warning(f"Invalid min_length: {min_length}")
                return self._set_min_length(input("Please enter a valid min_length: "))

            save = input(f"Save {min_length} as default min_length? (y/n): ")
            return min_length, save.lower()[0] == "y"

        return self._set_min_length(input("Please enter a valid min_length: "))

    def _get_max_length(self, max_length) -> Tuple[int, bool]:

        if max_length and max_length >= self.min_length:
            try:
                max_length = int(max_length)
            except ValueError:
                logger.warning(f"Invalid min_length: {max_length}")
                return self._set_min_length(input("Please enter a valid max_length: "))

            save = input(f"Save {max_length} as default max_length? (y/n): ")
            return max_length, save.lower()[0] == "y"

        return self._set_min_length(input("Please enter a valid max_length: "))

    def _set_numbers(self, numbers) -> Tuple[bool, bool]:

        if numbers:
            try:
                numbers = bool(numbers)
            except ValueError:
                logger.warning(f"Invalid numbers parameter value: {numbers}")
                return self._set_numbers(input("Please enter a valid value (True/False): "))

            save = input(f"Save {numbers} as default numbers? (y/n): ")
            return numbers, save.lower()[0] == "y"

        return self._set_numbers(input("Please enter a valid value (True/False): "))

    def _set_symbols(self, symbols) -> Tuple[bool, bool]:

        if symbols:
            try:
                symbols = bool(symbols)
            except ValueError:
                logger.warning(f"Invalid symbols parameter value: {symbols}")
                return self._set_symbols(input("Please enter a valid value (True/False): "))

            save = input(f"Save {symbols} as default symbols? (y/n): ")
            return symbols, save.lower()[0] == "y"

        return self._set_symbols(input("Please enter a valid value (True/False): "))

    def _set_uppercase(self, uppercase) -> Tuple[bool, bool]:

        if uppercase:
            try:
                uppercase = bool(uppercase)
            except ValueError:
                logger.warning(f"Invalid uppercase parameter value: {uppercase}")
                return self._set_uppercase(input("Please enter a valid value (True/False): "))

            save = input(f"Save {uppercase} as default uppercase? (y/n): ")
            return uppercase, save.lower()[0] == "y"

        return self._set_uppercase(input("Please enter a valid value (True/False): "))

    def _get_lowercase(self, lowercase) -> Tuple[bool, bool]:

        if lowercase:
            try:
                lowercase = bool(lowercase)
            except ValueError:
                logger.warning(f"Invalid lowercase parameter value: {lowercase}")
                return self._set_lowercase(input("Please enter a valid value (True/False): "))

            save = input(f"Save {lowercase} as default lowercase? (y/n): ")
            return lowercase, save.lower()[0] == "y"

        if not self.uppercase:
            logger.warning("At least one of the parameters uppercase or lowercase must be True")
            logger.info("Setting lowercase to True")
            return True, False
