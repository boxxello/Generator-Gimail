import argparse
import logging
import os
from argparse import Namespace
from datetime import datetime
from time import sleep

from fake_useragent import UserAgent, FakeUserAgentError

from cli.DriverManager import ALL_VALID_BROWSER_STRINGS, DriverManager
from cli.ScraperGimail import ScraperGmail
from generator_mail.CommonFN import CommonFN
from generator_mail.EmailGen import EmailGen
from generator_mail.PasswordGenerator import PasswordGenerator
from utils import Utilities
from utils.logging import get_logger
from cli.settings import Settings

logger = get_logger()


def enable_debug_logging() -> None:
    """
    Enable debug logging for the scripts

    :return: None
    """
    logger.setLevel(logging.DEBUG)
    for handler in logger.handlers:
        handler.setLevel(logging.DEBUG)
    logger.info(f"Enabled debug logging")


def run(browser: str, min_length: int, max_length: int,
        numbers: bool,  symbols: bool, uppercase: bool,
        lowercase: bool,number_of_accounts: int, delete_settings: bool, settings_file: str):



    settings = Settings(browser, min_length, max_length,
                        numbers, symbols, uppercase,
                        lowercase, number_of_accounts,delete_settings, settings_file)
    email_generator = EmailGen()
    password_generator = PasswordGenerator( min_length=settings.min_length,
                               max_length=settings.max_length, numbers=settings.numbers,
                               symbols=settings.symbols,uppercase= settings.uppercase,
                               lowercase=settings.lowercase)
    email_lists= email_generator.\
        _generate_n_emails(settings.number_of_accs)
    password_lists = password_generator._generate_n_passwords(settings.number_of_accs)
    file_name= f'email_pass{datetime.now().strftime("%H_%M_%S")}.json'
    path=os.path.join(Utilities.DATA_DIR_PATH,'generated_accs')
    os.makedirs(path,exist_ok=True)
    CommonFN.save_email_pass_as_json(email_lists, password_lists, os.path.join(path,file_name))
    print(email_lists)
    print(password_lists)

    for i in range(0,3):
        try:
            ua=UserAgent()
            user_agent_to_use=ua.random
            dm_obj = DriverManager(browser=settings.browser, proxy=,user_agent=user_agent_to_use)
            scraper = ScraperGmail(driver=dm_obj.driver, nationality='it', settings=settings)
            break
        except FakeUserAgentError:

            ua=None




def parse_args() -> Namespace:
    """
    Parse args from the CLI or use the args passed in

    :return: Args to be used in the script
    """

    parser = argparse.ArgumentParser(description='Gmail account generator')
    parser.add_argument(
        "--browser",
        required=False,
        type=str,
        choices=ALL_VALID_BROWSER_STRINGS,
        help="Browser to use to generate gmail accs",
    )
    parser.add_argument(
        "--debug",
        type=bool,
        default=True,
        help="Enable debug logging",
    )
    parser.add_argument(
        "--min_length",
        type=int,
        help="Set password min length",
    )
    parser.add_argument(
        "--max_length",
        type=int,
        help="Set password max length",
    )
    parser.add_argument(
        "--numbers",
        type=bool,
        help="Include numbers into the password",
    )
    parser.add_argument(
        "--symbols",
        type=bool,
        help="Include symbols into the password",
    )
    parser.add_argument(
        "--uppercase",
        type=bool,
        help="Include uppercase letters into the password",
    )
    parser.add_argument(
        "--lowercase",
        type=bool,
        help="Include lowercase letters into the password",
    )
    parser.add_argument(
        "--delete_settings",
        type=bool,
        help="Delete any existing settings file",
    )
    parser.add_argument(
        "--settings_file",
        type=bool,
        help="Path to the settings file",
    )
    parser.add_argument(
        "--number_of_accounts",
        type=int,
        help="Number of accounts to generate",
    )



    args = parser.parse_args()
    logger.info(args)

    return args


def main():
    args = parse_args()
    if args:
        if args.debug:
            enable_debug_logging()
        run(args.browser,
            args.min_length,
            args.max_length,
            args.numbers,
            args.symbols,
            args.uppercase,
            args.lowercase,
            args.number_of_accounts,
            args.delete_settings,
            args.settings_file)

