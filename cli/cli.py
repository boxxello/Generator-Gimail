import argparse
import logging
from argparse import Namespace

from cli.DriverManager import ALL_VALID_BROWSER_STRINGS, DriverManager
from generator_mail.EmailGen import EmailGen
from generator_mail.PasswordGenerator import PasswordGenerator
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


def run(browser: str):
    email_generator = EmailGen()
    password_generator = PasswordGenerator()

    settings = Settings()
    if browser:
        dm = DriverManager(browser=browser)


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
        default="chrome",
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

    args = parser.parse_args()
    logger.info(args)

    return args


def main():
    args = parse_args()
    if args:
        if args.debug:
            enable_debug_logging()
        run(args.browser)
