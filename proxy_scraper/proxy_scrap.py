"""Gather proxies from the providers without
   checking and save them to a file."""
import argparse
import asyncio
import re
import sys
import time
from enum import Enum

import httpx
import requests
from bs4 import BeautifulSoup

from utils.logging import get_logger

logger = get_logger()


# class ProxyScraper:
#     @staticmethod
#     def get_proxies():
#         session=requests.Session()
#         response=session.get("http://127.0.0.1:8000")
#         if response.status_code==200:
#             return response.json().get("proxies")

class Scraper:

    def __init__(self, method, _url):
        self.method = method
        self._url = _url

    def _get_url(self, **kwargs):
        return self._url.format(**kwargs, method=self.method)

    async def _get_response(self, client):
        return await client.get(self._get_url())

    async def _handle(self, response):
        return response.text

    async def _scrape(self, client):
        response = await self._get_response(client)
        proxies = await self._handle(response)
        pattern = re.compile(r"\d{1,3}(?:\.\d{1,3}){3}(?::\d{1,5})?")
        return re.findall(pattern, proxies)


# From spys.me
class SpysMeScraper(Scraper):

    def __init__(self, method):
        super().__init__(method, "https://spys.me/{mode}.txt")

    def _get_url(self, **kwargs):
        mode = "proxy" if self.method == "http" else "socks" if self.method == "socks" else "unknown"
        if mode == "unknown":
            raise NotImplementedError
        return super()._get_url(mode=mode, **kwargs)


# proxyscrape.com
class ProxyScrapeScraper(Scraper):

    def __init__(self, method, timeout=1000, country="All"):
        self.timout = timeout
        self.country = country
        super().__init__(method,
                         "https://api.proxyscrape.com/?request=getproxies"
                         "&proxytype={method}"
                         "&timeout={timout}"
                         "&country={country}")

    def _get_url(self, **kwargs):
        return super()._get_url(timout=self.timout, country=self.country, **kwargs)


class ProxyListDownloadScraper(Scraper):

    def __init__(self, method, anon):
        self.anon = anon
        super().__init__(method, "https://www.proxy-list.download/api/v1/get?type={method}&anon={anon}")

    def _get_url(self, **kwargs):
        return super()._get_url(anon=self.anon, **kwargs)


class GeneralTableScraper(Scraper):

    async def _handle(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        proxies = set()
        table = soup.find("table", attrs={"class": "table table-striped table-bordered"})
        for row in table.findAll("tr"):
            count = 0
            proxy = ""
            for cell in row.findAll("td"):
                if count == 1:
                    proxy += ":" + cell.text.replace("&nbsp;", "")
                    proxies.add(proxy)
                    break
                proxy += cell.text.replace("&nbsp;", "")
                count += 1
        return "\n".join(proxies)


scrapers = [
    SpysMeScraper("http"),
    SpysMeScraper("socks"),
    ProxyScrapeScraper("http"),
    ProxyScrapeScraper("socks4"),
    ProxyScrapeScraper("socks5"),
    ProxyListDownloadScraper("https", "elite"),
    ProxyListDownloadScraper("http", "elite"),
    ProxyListDownloadScraper("http", "transparent"),
    ProxyListDownloadScraper("http", "anonymous"),
    GeneralTableScraper("https", "http://sslproxies.org"),
    GeneralTableScraper("http", "http://free-proxy-list.net"),
    GeneralTableScraper("http", "http://us-proxy.org"),
    GeneralTableScraper("socks", "http://socks-proxy.net"),
]


class ProxyType(Enum):
    HTTP = "http"
    SOCKS4 = "socks4"
    SOCKS5 = "socks5"
    ALL = "all"


async def scrape(proxy_type: ProxyType):
    now = time.time()
    if proxy_type == ProxyType.ALL:
        proxy_type = ["http", "socks4", "socks5"]
    elif proxy_type == ProxyType.SOCKS4 or proxy_type == ProxyType.SOCKS5:
        proxy_type += ["socks4", "socks5"]
    elif proxy_type == ProxyType.HTTP:
        proxy_type += ["http"]
    proxy_scrapers = [s for s in scrapers if s.method in proxy_type]
    if not proxy_scrapers:
        raise ValueError("Method not supported")
    logger.info("Scraping proxies...")
    proxies = []

    tasks = []
    client = httpx.AsyncClient(follow_redirects=True)

    async def scrape_scraper(scraper: Scraper):
        logger.info(f"Looking {scraper._get_url()}...")
        proxies.extend(await scraper._scrape(client))

    for scraper in proxy_scrapers:
        tasks.append(asyncio.ensure_future(scrape_scraper(scraper)))

    await asyncio.gather(*tasks)
    await client.aclose()

    logger.info(f"Writing {len(proxies)} proxies to file...")
    with open("output.txt", "w") as f:
        f.write("\n".join(proxies))
    logger.info("Done!")
    logger.info(f"Took {time.time() - now} seconds")
    return proxies


if __name__ == "__main__":
    print(asyncio.run(scrape(ProxyType.ALL)))
