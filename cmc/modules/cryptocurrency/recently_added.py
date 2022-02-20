#!/usr/bin/env python

"""Module for fetching data of Cryptocurrencies which were recently
added in the last 24 hours on CoinMarketCap website."""

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
from cmc.utils.models import RecentlyAddedData


class RecentlyAdded(CMCBaseClass):
    """Class for scraping the data of CryptoCurrencies that appear
    in the recently added table."""

    def __init__(self, proxy: Optional[str] = None, as_dict: bool = False) -> None:
        """
        Args:
            proxy (Optional[str], optional): Proxy to be used for Selenium and requests Session. Defaults to None.
            as_dict (bool): Return the data as a dictionary. Defaults to False.
        """
        super().__init__(proxy)
        self.base_url = "https://coinmarketcap.com/new/"
        self.out = as_dict

    @property
    def __get_page_data(self) -> bs4.BeautifulSoup:
        """Scrape the table from recently added CryptoCurrencies page data
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
                '//*[@id="__next"]/div/div[1]/div[2]/div/div[2]/table/tbody',
            )
            page_data = result.get_attribute("innerHTML")
            driver.quit()
            soup = BeautifulSoup(page_data, features="lxml")
            return soup
        except:
            raise ScrapeError

    @property
    def get_data(
        self,
    ) -> Union[Dict[int, Dict[str, Any]], Dict[int, RecentlyAddedData]]:
        """Scrape the CryptoCurrencies which are recently added in the
        last 24 hours.

        Returns:
            Union[Dict[int, Dict[str, Any]], Dict[int, RecentlyAddedData]]: Scraped data of trending CryptoCurrencies.
        """
        recently_added: Dict[int, Any] = {}
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
                    percent_1h: Tuple[str, ...] = (
                        "down",
                        td[4].find("span", class_="sc-15yy2pl-0 hzgCfk").text,
                    )
            except:
                percent_1h: Tuple[str, ...] = (  # type: ignore
                    "up",
                    td[4].find("span", class_="sc-15yy2pl-0 kAXKAX").text,
                )
            try:
                if td[5].find("span", class_="sc-15yy2pl-0 hzgCfk").span["class"][0]:
                    percent_24h: Tuple[str, ...] = (
                        "down",
                        td[5].find("span", class_="sc-15yy2pl-0 hzgCfk").text,
                    )
            except:
                percent_24h: Tuple[str, ...] = (  # type: ignore
                    "up",
                    td[5].find("span", class_="sc-15yy2pl-0 kAXKAX").text,
                )
            fully_diluted_market_cap: str = td[6].text
            volume_24h: str = td[7].text
            blockchain: str = td[8].find("div", class_="s8fs2i-2 TBaWj").text
            added: str = td[9].text
            result = {
                "name": name,
                "symbol": symbol,
                "cmc_name": cmc_link.split("/")[-2],
                "url": self.cmc_url + cmc_link,
                "price": price,
                "percent_1h": percent_1h,
                "percent_24h": percent_24h,
                "fully_diluted_market_cap": fully_diluted_market_cap,
                "volume_24h": volume_24h,
                "blockchain": blockchain,
                "added": added,
                "timestamp": datetime.now(),
            }
            if self.out:
                recently_added[num + 1] = result
            else:
                recently_added[num + 1] = RecentlyAddedData(**result)
        return recently_added
