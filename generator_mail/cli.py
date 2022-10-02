import argparse
import logging
from argparse import Namespace

from generator_mail.DriverManager import ALL_VALID_BROWSER_STRINGS, DriverManager
from generator_mail.logging import get_logger
from generator_mail.settings import Settings

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

def run(browser:str):
    settings=Settings()
    if browser:
        dm = DriverManager(browser=browser)


def parse_args() -> Namespace:
    """
    Parse args from the CLI or use the args passed in

    :return: Args to be used in the script
    """

    parser=argparse.ArgumentParser(description='Gmail account generator')
    parser.add_argument(
        "--browser",
        required=False,
        type=str,
        choices=ALL_VALID_BROWSER_STRINGS,
        default="chrome",
        help="Browser to use to generate gmail accs",
    )
    args=parser.parse_args()
    logger.info(args)
    return args


def main():
    args = parse_args()
    if args:
        if args.debug:
            enable_debug_logging()
        run(args.browser)