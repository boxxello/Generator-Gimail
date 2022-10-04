import os
from typing import Tuple

from ruamel.yaml import dump, YAML

from cli.DriverManager import ALL_VALID_BROWSER_STRINGS
from utils.utils import Utilities
from utils.logging import get_logger

logger = get_logger()


class Settings:
    def __init__(self, browser, min_length, max_length, numbers, symbols, uppercase, lowercase, delete_settings, settings_file_path: str = "settings.yaml"):
        # set_browser returns a Tuple[str, bool] where str = browser and parameter and bool = True if browser
        # should be saved as default.
        # The same logic is applied to all "_set_x" methods
        self.browser, self.save_browser = self._set_browser(browser)
        self.min_length, self.save_min_length = self._set_min_length(min_length)
        self.max_length, self.save_max_length = self._get_max_length(max_length)
        self.numbers, self.save_numbers = self._set_numbers(numbers)
        self.symbols, self.save_symbols = self._set_symbols(symbols)
        self.uppercase, self.save_uppercase = self._set_uppercase(uppercase)
        self.lowercase, self.save_lowercase = self._set_lowercase(lowercase)

        self.should_store_parameters = False
        if delete_settings:
            self.delete_settings()
        self._settings_file_path = os.path.join(Utilities.get_app_dir(), settings_file_path)
        self._init_settings()

    def _init_settings(self) -> None:
        """
           Initialize the settings to be used in the script

           :return:
        """

        settings = self._load_user_settings()
        if settings is None:
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
        if max_length and max_length >= self.min_length:
            try:
                max_length = int(max_length)
            except ValueError:
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

    def _set_lowercase(self, lowercase) -> Tuple[bool, bool]:
        """
        Sets the lowercase parameter
        """
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

    def _save_settings(self) -> None:
        """
        Confirm if the user wants to save settings to file

        :return:
        """
        yaml_structure = {
            "generator-gmail": {
                "numbers": str(self.numbers) if self.should_store_parameters else None,
                "lowercase": str(self.lowercase) if self.should_store_parameters else None,
                "uppercase": str(self.uppercase) if self.should_store_parameters else None,
                "symbols": self.symbols if self.should_store_parameters else None,
                "min_length": str(self.min_length) if self.should_store_parameters else None,
                "max_length": str(self.max_length) if self.should_store_parameters else None,
            }
        }
        with open(self._settings_file_path, "w+") as f:
            dump(yaml_structure, stream=f)
        logger.info(f"Saved your settings in {self._settings_file_path}")

        if not self.should_store_parameters:
            logger.info(f"Your parameters have not been saved to settings.")

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


