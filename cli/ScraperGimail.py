import datetime
import json
import os
from typing import Dict, List

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from cli.settings import Settings
from mac_generator.Generator import GeneratorMac
from utils.logging import get_logger

logger = get_logger()


class ScraperGmail:
    def __init__(self, driver: WebDriver, settings: Settings, nationality: str):
        self.site = f"www.google.com/intl/{nationality}/gmail/about/"
        self.DOMAIN_BUSINESS_FULL = f"https://{self.site}"
        self.scraper_name = "gmail.gen"
        self.cookie_file = None
        self.driver = driver
        self.settings = settings
        self.HEADERS = {
            "origin": f"",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "Content-Type": "application/json;charset=utf-8",
            "x-requested-with": "XMLHttpRequest",
            "x-checkout-version": "2",
            "referer": f"",
            "authority": f""
        }
        self.session = requests.Session()
        self._init_driver()
        self._login()

    def _init_driver(self):
        self.session.headers = self.HEADERS
        cookie_details = self._load_cookies()
        if cookie_details is None:
            pass

    def _cache_cookies(self, cookies: List) -> None:
        """
        Caches cookies for future logins
        :param cookies:
        :return:
        """
        logger.info("Caching cookie for future use")
        with open(self.cookie_file, "w") as f:
            json.dump(cookies, f)

    def _load_cookies(self) -> Dict:
        """
        Loads existing cookie file

        :return:
        Dict
        """
        cookies = None
        if self.cookie_file:
            if os.path.isfile(self.cookie_file):
                logger.info("Loading cookie from file")
                with open(self.cookie_file) as f:
                    cookies = json.loads(f.read())
                    return cookies
            else:
                logger.info("No cookie available")
        else:
            logger.info("No cookie file specified")

    def _delete_cookies(self) -> None:
        """
        Remove existing cookie file

        :return:
        """
        logger.info("Deleting cookie")
        os.remove(self.cookie_file)

    @staticmethod
    def time_run(func):
        async def wrapper(self):
            start_time = datetime.datetime.utcnow()
            try:
                response = await func(self)
            except Exception as e:
                logger.error(f"Error while running scraper: {e}", exc_info=True)
                return []
            end_time = datetime.datetime.utcnow()
            logger.info(
                f"Function finished in {(end_time - start_time).total_seconds():.2f} seconds"
            )
            return response

        return wrapper

    def _login(self):
        self.driver.get(self.DOMAIN_BUSINESS_FULL)
        self._find_login_btn()

    def _find_login_btn(self):

        self.driver.get(self.DOMAIN_BUSINESS_FULL)

        login_btn = '//a[@data-action="sign in"]'
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, login_btn))
        ).click()
