#!/usr/bin/env python

"""Module for fetching data of Cryptocurrencies which were trending
in the last 24 hours on CoinMarketCap website."""

from datetime import datetime
import os
import time
from typing import Any, Dict, List, Optional, Tuple, Union
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from cmc.modules.base import CMCBaseClass
from cmc.utils.exceptions import ScrapeError
from cmc.utils.models import TrendingData


class Trending(CMCBaseClass):
    """Class for scraping the data of CryptoCurrencies that appear
    in the trending table."""

    def __init__(self, proxy: Optional[str] = None, as_dict: bool = False) -> None:
        """
        Args:
            proxy (Optional[str], optional): Proxy to be used for Selenium and requests Session. Defaults to None.
            as_dict (bool): Return the data as a dictionary. Defaults to False.
        """
        super().__init__(proxy)
        self.base_url = "https://coinmarketcap.com/trending-cryptocurrencies/"
        self.out = as_dict

    @property
    def __get_page_data(self) -> bs4.BeautifulSoup:
        """Scrape the table from trending CryptoCurrencies page data
        and return the scraped data.

        Raises:
            ScrapeError: Raised when data cannot be scraped from the webpage.

        Returns:
            bs4.BeautifulSoup: Scraped page data.
        """
        driver = webdriver.Chrome(
            service=self.service,
            options=self.driver_options,
            service_log_path=os.devnull,
        )
        try:
            driver.get(self.base_url)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            result = driver.find_element(
                By.XPATH,
                '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[2]/table/tbody',
            )
            page_data = result.get_attribute("innerHTML")
            driver.quit()
            soup = BeautifulSoup(page_data, features="lxml")
            return soup
        except:
            raise ScrapeError

    @property
    def get_data(self) -> Union[Dict[int, Dict[str, Any]], Dict[int, TrendingData]]:
        """Scrape the CryptoCurrencies which are trending in the
        last 24 hours.

        Returns:
            Union[Dict[int, Dict[str, Any]], Dict[int, TrendingData]]: Scraped data of trending CryptoCurrencies.
        """
        trending: Dict[int, Any] = {}
        page_data = self.__get_page_data
        data = page_data.find_all("tr")
        for num, content in enumerate(data):
            td = content.find_all("td")
            name: str = td[2].find("p", class_="sc-1eb5slv-0 iworPT").text
            symbol: str = (
                td[2].find("p", class_="sc-1eb5slv-0 gGIpIK coin-item-symbol").text
            )
            cmc_link: str = td[2].find("a", class_="cmc-link")["href"]
            try:
                price: str = td[3].find("div", class_="sc-131di3y-0 cLgOOr").text
            except:
                price: str = td[3].span.text  # type: ignore
            try:
                if td[4].find("span", class_="sc-15yy2pl-0 hzgCfk").span["class"][0]:
                    percent_24h: Tuple[str, ...] = (
                        "down",
                        td[4].find("span", class_="sc-15yy2pl-0 hzgCfk").text,
                    )
            except:
                percent_24h: Tuple[str, ...] = (  # type: ignore
                    "up",
                    td[4].find("span", class_="sc-15yy2pl-0 kAXKAX").text,
                )
            try:
                if td[5].find("span", class_="sc-15yy2pl-0 hzgCfk").span["class"][0]:
                    percent_7d: Tuple[str, ...] = (
                        "down",
                        td[5].find("span", class_="sc-15yy2pl-0 hzgCfk").text,
                    )
            except:
                percent_7d: Tuple[str, ...] = (  # type: ignore
                    "up",
                    td[5].find("span", class_="sc-15yy2pl-0 kAXKAX").text,
                )
            try:
                if td[6].find("span", class_="sc-15yy2pl-0 hzgCfk").span["class"][0]:
                    percent_30d: Tuple[str, ...] = (
                        "down",
                        td[6].find("span", class_="sc-15yy2pl-0 hzgCfk").text,
                    )
            except:
                percent_30d: Tuple[str, ...] = (  # type: ignore
                    "up",
                    td[6].find("span", class_="sc-15yy2pl-0 kAXKAX").text,
                )
            try:
                market_cap: str = td[7].find("p", class_="sc-1eb5slv-0 bZMzMD").text
            except:
                market_cap: str = td[7].text  # type: ignore
            volume_24h: str = td[8].text
            result = {
                "name": name,
                "symbol": symbol,
                "cmc_name": cmc_link.split("/")[-2],
                "url": self.cmc_url + cmc_link,
                "price": price,
                "percent_24h": percent_24h,
                "percent_7d": percent_7d,
                "percent_30d": percent_30d,
                "market_cap": market_cap,
                "volume_24h": volume_24h,
                "timestamp": datetime.now(),
            }
            if self.out:
                trending[num + 1] = result
            else:
                trending[num + 1] = TrendingData(**result)
        return trending
