from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager

from cli.add_proxy import get_proxy_extension
from utils.logger import get_logger

logger = get_logger()
VALID_FIREFOX_STRINGS = {"ff", "firefox"}
VALID_CHROME_STRINGS = {"chrome", "google-chrome"}
VALID_CHROMIUM_STRINGS = {"chromium"}
VALID_INTERNET_EXPLORER_STRINGS = {"internet_explorer", "ie"}
VALID_EDGE_STRINGS = {"edge"}

ALL_VALID_BROWSER_STRINGS = VALID_CHROME_STRINGS.union(VALID_CHROMIUM_STRINGS)


class DriverManager:
    def __init__(self, browser: str, proxy: str = None, user_agent: str = None):
        self.driver: webdriver = None
        self.options = None
        self.browser = browser
        self.proxy=proxy
        self.user_agent=user_agent
        self._init_driver()


    def _init_driver(self):
        """
        Initialize the correct web driver based on the users requested browser

        :return: None
        """

        if self.browser.lower() in VALID_CHROME_STRINGS:
            # enabling performance and request profiling
            caps = DesiredCapabilities.CHROME
            # as per latest docs
            caps['goog:loggingPrefs'] = {'performance': 'ALL'}
            # disabling the annoying chrome notification
            self.options = webdriver.ChromeOptions()
            self.options.add_argument("--mute-audio")
            self.options.add_experimental_option("useAutomationExtension", False)
            self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
            # self.options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
            if self.proxy:
                if '@' in self.proxy:
                    parts = self.proxy.split('@')

                    user = parts[0].split(':')[0]
                    pwd = parts[0].split(':')[1]

                    host = parts[1].split(':')[0]
                    port = parts[1].split(':')[1]

                    extension = get_proxy_extension(PROXY_HOST=host, PROXY_PORT=port, PROXY_USER=user, PROXY_PASS=pwd)
                    self.options.add_extension(extension)
                else:
                    self.options.add_argument(f'--proxy-server=http://{self.proxy}')
            if self.user_agent:
                self.options.add_argument(f'--user-agent={self.user_agent}')
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options,
                                           desired_capabilities=caps)



        elif self.browser.lower() in VALID_CHROMIUM_STRINGS:
            self.driver = webdriver.Chrome(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            )
        elif self.browser.lower() in VALID_EDGE_STRINGS:
            self.driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        elif self.browser.lower() in VALID_FIREFOX_STRINGS:
            self.driver = webdriver.Firefox(
                executable_path=GeckoDriverManager().install()
            )
        elif self.browser.lower() in VALID_INTERNET_EXPLORER_STRINGS:
            self.driver = webdriver.Ie(IEDriverManager().install())
        else:
            raise ValueError("No matching browser found")

        # Get around captcha
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": "const newProto = navigator.__proto__;"
                          "delete newProto.webdriver;"
                          "navigator.__proto__ = newProto;"
            },
        )
        # Maximize the browser
        self.driver.maximize_window()
