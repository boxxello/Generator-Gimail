import os
from typing import Tuple

from ruamel.yaml import dump, YAML

from cli.DriverManager import ALL_VALID_BROWSER_STRINGS
from utils.utils import Utilities
from utils.logging import get_logger

logger = get_logger()


class Settings:
    def __init__(self, browser, min_length, max_length, numbers, symbols, uppercase, lowercase, number_of_accs,
                 delete_settings, settings_file_path=None):
        # set_browser returns a Tuple[str, bool] where str = browser and parameter and bool = True if browser
        # should be saved as default.
        # The same logic is applied to all "_set_x" methods
        if settings_file_path is None:
            settings_file_path = 'settings.yaml'

        self._settings_file_path = os.path.join(Utilities.get_app_dir(), settings_file_path)
        if delete_settings:
            self.delete_settings()
        settings = self._load_user_settings()
        # TODO::Refactorize these next lines, they're ugly af.
        if settings is not None:
            if settings.get('browser') is None:
                self.browser, self.save_browser = self._set_browser(browser)
            else:
                self.browser = settings['browser']
                self.save_browser = False
            if settings.get('min_length') is None:
                self.min_length, self.save_min_length = self._set_min_length(min_length)
            else:
                self.min_length = settings['min_length']
                self.save_min_length = False
            if settings.get('max_length') is None:
                self.max_length, self.save_max_length = self._get_max_length(max_length)
            else:
                self.max_length = settings['max_length']
                self.save_max_length = False
            if settings.get('numbers') is None:
                self.numbers, self.save_numbers = self._set_numbers(numbers)
            else:
                self.numbers = settings['numbers']
                self.save_numbers = False
            if settings.get('symbols') is None:
                self.symbols, self.save_symbols = self._set_symbols(symbols)
            else:
                self.symbols = settings['symbols']
                self.save_symbols = False
            if settings.get('uppercase') is None:
                self.uppercase, self.save_uppercase = self._set_uppercase(uppercase)
            else:
                self.uppercase = settings['uppercase']
                self.save_uppercase = False

            if settings.get('lowercase') is None:
                self.lowercase, self.save_lowercase = self._set_lowercase(lowercase)
            else:
                self.lowercase = settings['lowercase']
                self.save_lowercase = False
            if settings.get('number_of_accs') is None:
                self.number_of_accs, self.save_number_of_accs = self._set_number_of_accs(number_of_accs)
            else:
                self.number_of_accs = settings['number_of_accs']
                self.save_number_of_accs = False
        else:
            self.browser, self.save_browser = self._set_browser(browser)
            self.min_length, self.save_min_length = self._set_min_length(min_length)
            self.max_length, self.save_max_length = self._get_max_length(max_length)
            self.numbers, self.save_numbers = self._set_numbers(numbers)
            self.symbols, self.save_symbols = self._set_symbols(symbols)
            self.uppercase, self.save_uppercase = self._set_uppercase(uppercase)
            self.lowercase, self.save_lowercase = self._set_lowercase(lowercase)
            self.number_of_accs, self.save_number_of_accs = self._set_number_of_accs(number_of_accs)
        self._save_settings()

    def delete_settings(self) -> None:
        """
        Delete the settings file

        :return: None
        """
        if os.path.isfile(self._settings_file_path):
            delete_settings = input(
                "Please confirm that you want to delete your saved settings (Y/N): "
            )
            if delete_settings.lower() == "y":
                os.remove(self._settings_file_path)
                logger.info(f"Settings file deleted: {self._settings_file_path}")
        else:
            logger.info("No settings to delete")

    def _set_browser(self, browser) -> Tuple[str, bool]:
        """
        Sets the browser parameter
        """
        if not browser or browser not in ALL_VALID_BROWSER_STRINGS:
            logger.warning(f"Invalid browser: {browser}")
            logger.info(f"Valid browsers: {ALL_VALID_BROWSER_STRINGS}")
            return self._set_browser(input("Please enter a valid browser: "))

        save = input(f"Save {browser} as default browser? (y/n): ")

        return browser, save.lower()[0] == "y"

    def _set_min_length(self, min_length) -> Tuple[int, bool]:
        """
        Sets the min-length parameter
        :param min_length:
        """
        if min_length:
            try:
                min_length = int(min_length)
            except ValueError:
                logger.warning(f"Invalid min_length: {min_length}")
                return self._set_min_length(input("Please enter a valid min_length: "))

            save = input(f"Save {min_length} as default min_length? (y/n): ")
            print(save.lower()[0])
            return min_length, save.lower()[0] == "y"

        return self._set_min_length(input("Please enter a valid min_length: "))

    def _get_max_length(self, max_length) -> Tuple[int, bool]:
        """
        Sets the max-length parameter
        """
        if max_length:
            try:
                max_length = int(max_length)
            except ValueError:
                logger.warning(f"Invalid min_length: {max_length}")
                return self._get_max_length(input("Please enter a valid max_length: "))
            if max_length < self.min_length:
                logger.warning(f"Invalid min_length: {max_length}")
                return self._get_max_length(input("Please enter a valid max_length: "))
            save = input(f"Save {max_length} as default max_length? (y/n): ")
            return max_length, save.lower()[0] == "y"

        return self._get_max_length(input("Please enter a valid max_length: "))

    def _set_numbers(self, numbers) -> Tuple[bool, bool]:
        """
        Sets the numbers parameter
        """
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
        """
        Sets the symbols parameter
        """
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
        """
        Sets the uppercase parameter
        """
        if uppercase:
            try:
                uppercase = bool(uppercase)
            except ValueError:
                logger.warning(f"Invalid uppercase parameter value: {uppercase}")
                return self._set_uppercase(input("Please enter a valid value (True/False): "))

            save = input(f"Save {uppercase} as default uppercase? (y/n): ")
            return uppercase, save.lower()[0] == "y"

        return self._set_uppercase(input("Please enter a valid value (True/False): "))

    def _set_number_of_accs(self, number_of_accs):
        """
        sets the number of accounts to be created
        :param number_of_accs:
        """
        if number_of_accs:
            try:
                number_of_accs = int(number_of_accs)
            except ValueError:
                logger.warning(f"Invalid min_length: {number_of_accs}")
                return self._set_number_of_accs(input("Please enter a valid number of accs to be generated: "))

            save = input(f"Save {number_of_accs} as default min_length? (y/n): ")
            print(save.lower()[0])
            return number_of_accs, save.lower()[0] == "y"

        return self._set_number_of_accs(input("Please enter a valid min_length: "))

    def _set_lowercase(self, lowercase) -> Tuple[bool, bool]:
        """
        Sets the lowercase parameter
        """
        if lowercase:
            try:
                lowercase = bool(lowercase)
                if not self.uppercase:
                    logger.warning("At least one of the parameters uppercase or lowercase must be True")
                    logger.info("Setting lowercase to True")
                    return True, False
            except ValueError:
                logger.warning(f"Invalid lowercase parameter value: {lowercase}")
                return self._set_lowercase(input("Please enter a valid value (True/False): "))

            print(lowercase)
            save = input(f"Save {lowercase} as default lowercase? (y/n): ")
            return lowercase, save.lower()[0] == "y"

        return self._set_lowercase(input("Please enter a valid value (True/False): "))

    def _save_settings(self) -> None:
        """
        Saves settings to settings file

        :return:
        """
        yaml_structure = {
            "generator-gmail": {
                "numbers": self.numbers if self.save_numbers else None,
                "lowercase": str(self.lowercase) if self.save_lowercase else None,
                "uppercase": str(self.uppercase) if self.save_uppercase else None,
                "symbols": self.symbols if self.save_symbols else None,
                "min_length": self.min_length if self.save_min_length else None,
                "max_length": self.max_length if self.save_max_length else None,
            }
        }
        with open(self._settings_file_path, "w+") as f:
            dump(yaml_structure, stream=f)
        logger.info(f"Saved your settings in {self._settings_file_path}")

    def _load_user_settings(self):
        """
        Loads the settings from the yaml file if it exists

        :return: dictionary containing the script settings
        """
        yaml = YAML()

        settings = None
        if os.path.isfile(self._settings_file_path):
            logger.info("Loading existing settings")
            with open(self._settings_file_path) as f:
                settings = yaml.load(f)
            udemy_settings = settings["generator-gmail"]
            self.numbers = udemy_settings["lowercase"]
            self.uppercase = udemy_settings["uppercase"]
            self.symbols = udemy_settings["symbols"]
            self.min_length = udemy_settings.get("min_length")
            self.max_length = udemy_settings.get("max_length")

        return settings
