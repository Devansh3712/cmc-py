#!/usr/bin/env python

"""Module for fetching CryptoCurrency rankings from CoinMarketCap website."""

from datetime import datetime
import os
import time
from typing import Any, Dict, List, Optional, Union
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from cmc.modules.base import CMCBaseClass
from cmc.utils.exceptions import InvalidPageURL
from cmc.utils.models import RankingData


class Ranking(CMCBaseClass):
    """Class for scraping cryptocurrency ranking. Each page
    contains <= 100 cryptocurrencies.
    """

    def __init__(
        self,
        pages: List[int] = [1],
        ratelimit: int = 2,
        proxy: Optional[str] = None,
        as_dict: bool = False,
    ) -> None:
        """
        Args:
            pages (List[int], optional): Pages to scrape data from. Defaults to [1].
            ratelimit (int, optional): Ratelimit for parsing each page. Defaults to 2 seconds.
            proxy (Optional[str], optional): Proxy to be used for Selenium and requests Session. Defaults to None.
            as_dict (bool): Return the data as a dictionary. Defaults to False.
        """
        super().__init__(proxy)
        self.base_url = "https://coinmarketcap.com/?page="
        self.ratelimit = ratelimit
        self.pages = pages
        self.out = as_dict

    @property
    def get_data(
        self,
    ) -> Union[Dict[int, Dict[int, Dict[str, Any]]], Dict[int, Dict[int, RankingData]]]:
        """Get a dictionary of cryptocurrency ranks with page number as keys
        and rankings as values.

        Returns:
            Union[Dict[int, Dict[int, Dict[str, Any]]], Dict[int, Dict[int, RankingData]]]: Cryptocurrency rankings of all pages.
        """
        ranks: Dict[int, Dict[int, Any]] = {}
        for page in self.pages:
            start_rank = (page - 1) * 100
            page_data = self.__get_page_data(page)
            ranks[page] = self.__get_cryptocurrency_ranks(page_data, start_rank)
            start_rank += len(ranks[page])
            time.sleep(self.ratelimit)
        return ranks

    def __check_cryptocurrency_url(self, page_data: str) -> bool:
        """Check whether a webpage exists or not.

        Args:
            page_data (str): Scraped page data of the CryptoCurrency.

        Returns:
            bool: True if page exists else False.
        """
        soup = BeautifulSoup(page_data, features="lxml")
        error_message = soup.find_all("p", class_="sc-1eb5slv-0 liZSnj")
        if error_message == []:
            return True
        return False

    def __get_page_data(self, page: int) -> bs4.BeautifulSoup:
        """Scrape a single ranking page from CoinMarketCap.
        Uses selenium to load javascript elements of the website.

        Args:
            page (int): Page to scrape.

        Raises:
            InvalidPageURL: Raised when the URL is not valid.

        Returns:
            bs4.BeautifulSoup: Scraped website data.
        """
        driver = webdriver.Chrome(
            service=self.service,
            options=self.driver_options,
            service_log_path=os.devnull,
        )
        try:
            driver.get(self.base_url + str(page))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            result = driver.find_element(
                By.XPATH,
                '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[5]/table/tbody',
            )
            page_data = result.get_attribute("innerHTML")
            driver.quit()
            if not self.__check_cryptocurrency_url(page_data):
                raise InvalidPageURL(self.base_url + str(page))
            soup = BeautifulSoup(page_data, features="lxml")
            return soup
        except:
            raise InvalidPageURL(self.base_url + str(page))

    def __get_cryptocurrency_ranks(
        self, page_data: bs4.element.Tag, start_rank: int
    ) -> Union[Dict[int, Dict[str, Any]], Dict[int, RankingData]]:
        """Scrape cryptocurrency names and ranks from data returned by
        the __get_page_data() method.

        Args:
            page_data (bs4.element.Tag): Scraped page data.
            start_rank (int): Rank to start storing from.

        Returns:
            Union[Dict[int, Dict[str, Any]], Dict[int, RankingData]]: Cryptocurrency rankings of the current page.
        """
        cryptocurrency_ranking: Dict[int, Any] = {}
        data = page_data.find_all("tr")
        for rank, content in enumerate(data):
            td = content.find_all("td")[2]
            try:
                name: str = td.find_all("span")[1].text
            except:
                name: str = td.find("p", class_="sc-1eb5slv-0 iworPT").text  # type: ignore
            try:
                symbol: str = (
                    td.find("a", class_="cmc-link")
                    .find("p", class_="sc-1eb5slv-0 gGIpIK coin-item-symbol")
                    .text
                )
            except:
                symbol: str = td.find("a", class_="cmc-link").find("span", class_="crypto-symbol").text  # type: ignore
            cmc_link: str = td.find("a", class_="cmc-link")["href"]
            result = {
                "name": name,
                "symbol": symbol,
                "cmc_name": cmc_link.split("/")[-2],
                "url": self.cmc_url + cmc_link,
                "timestamp": datetime.now(),
            }
            if self.out:
                cryptocurrency_ranking[start_rank + rank + 1] = result
            else:
                cryptocurrency_ranking[start_rank + rank + 1] = RankingData(**result)
        return cryptocurrency_ranking
