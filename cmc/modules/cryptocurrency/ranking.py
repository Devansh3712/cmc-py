#!/usr/bin/env python

"""Module for fetching CryptoCurrency rankings from CoinMarketCap
website. Data is scraped through Selenium (to load JavaScript components)
and BeautifulSoup (to parse website data).
"""

import os
import time
from typing import Any, Dict, List, Optional
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from cmc.modules.base import CMCBaseClass


class Ranking(CMCBaseClass):
    """Class for scraping cryptocurrency ranking. Each page
    contains <= 100 cryptocurrencies.
    """

    def __init__(
        self, pages: List[int] = [1], ratelimit: int = 2, proxy: Optional[str] = None
    ) -> None:
        """
        Args:
            pages (List[int], optional): Pages to scrape data from. Defaults to [1].
            ratelimit (int, optional): Ratelimit for parsing each page. Defaults to 2 seconds.
            proxy (Optional[str], optional): Proxy to be used for Selenium and
            requests Session. Defaults to None.
        """
        super().__init__(proxy)
        self.base_url = "https://coinmarketcap.com/?page="
        self.ratelimit = ratelimit
        self.pages = pages

    @property
    def get_data(self) -> Dict[int, Dict[int, Dict[str, str]]]:
        """Get a dictionary of cryptocurrency ranks with page number as keys
        and rankings as values.

        Returns:
            Dict[int, Dict[int, Dict[str, str]]]: Cryptocurrency rankings
            of all pages.
        """
        ranks: Dict[int, Dict[int, Dict[str, str]]] = {}
        for page in self.pages:
            start_rank = (page - 1) * 100
            page_data = self.__get_page_data(page)
            ranks[page] = self.__get_cryptocurrency_ranks(page_data, start_rank)
            start_rank += len(ranks[page])
            time.sleep(self.ratelimit)
        return ranks

    def __get_page_data(self, page: int) -> bs4.BeautifulSoup:
        """Scrape a single ranking page from CoinMarketCap.
        Uses selenium to load javascript elements of the website.

        Args:
            page (int): Page to scrape.

        Returns:
            bs4.BeautifulSoup: Scraped website data.
        """
        driver = webdriver.Chrome(
            service=self.service,
            options=self.driver_options,
            service_log_path=os.devnull,
        )
        driver.get(self.base_url + str(page))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        result = driver.find_element(
            By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[5]/table/tbody'
        )
        page_data = result.get_attribute("innerHTML")
        driver.quit()
        soup = BeautifulSoup(page_data, features="lxml")
        return soup

    def __get_cryptocurrency_ranks(
        self, page_data: bs4.element.Tag, start_rank: int
    ) -> Dict[int, Dict[str, str]]:
        """Scrape cryptocurrency names and ranks from data returned by
        the get_page_data() method.

        Args:
            page_data (bs4.element.Tag): Scraped page data.
            start_rank (int): Rank to start storing from.

        Returns:
            Dict[int, Dict[str, Dict[str, str]]]: Cryptocurrency rankings of
            the current page.
        """
        cryptocurrency_ranking: Dict[int, Dict[str, str]] = {}
        data = page_data.find_all("tr")
        for rank, content in enumerate(data):
            td = content.find_all("td")[2]
            cryptocurrency = td.find_all(
                "div", class_="sc-16r8icm-0 sc-1teo54s-1 dNOTPP"
            )
            if cryptocurrency == []:
                name: str = td.find_all("span")[1].text
            else:
                name: str = cryptocurrency[0].find("p", class_="sc-1eb5slv-0 iworPT").text  # type: ignore
            try:
                symbol: str = (
                    td.find("a", class_="cmc-link")
                    .find("p", class_="sc-1eb5slv-0 gGIpIK coin-item-symbol")
                    .text
                )
            except:
                symbol: str = td.find("a", class_="cmc-link").find("span", class_="crypto-symbol").text  # type: ignore
            cmc_link: str = td.find("a", class_="cmc-link")["href"]
            cryptocurrency_ranking[start_rank + rank + 1] = {
                "name": name,
                "symbol": symbol,
                "cmc_name": cmc_link.split("/")[-2],
                "url": self.cmc_url + cmc_link,
            }
        return cryptocurrency_ranking
