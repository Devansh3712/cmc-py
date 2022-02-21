#!/usr/bin/env python

"""Module for fetching data of Cryptocurrencies which were the top losers
in the last 24 hours on CoinMarketCap website."""

from datetime import datetime
import os
import time
from typing import Any, Dict, List, Optional, Union
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from cmc.modules.base import CMCBaseClass
from cmc.utils.exceptions import ScrapeError
from cmc.utils.models import TopLosersData


class TopLosers(CMCBaseClass):
    """Class for scraping the data of CryptoCurrencies that appear
    in the top losers table."""

    def __init__(self, proxy: Optional[str] = None, as_dict: bool = False) -> None:
        """
        Args:
            proxy (Optional[str], optional): Proxy to be used for Selenium and requests Session. Defaults to None.
            as_dict (bool): Return the data as a dictionary. Defaults to False.
        """
        super().__init__(proxy)
        self.base_url = "https://coinmarketcap.com/gainers-losers/"
        self.out = as_dict

    @property
    def __get_page_data(self) -> bs4.BeautifulSoup:
        """Scrape the losers table from gainers-losers page data
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
                '//*[@id="__next"]/div/div[1]/div[2]/div/div[2]/div/div[2]/div/table/tbody',
            )
            page_data = result.get_attribute("innerHTML")
            driver.quit()
            soup = BeautifulSoup(page_data, features="lxml")
            return soup
        except:
            raise ScrapeError

    @property
    def get_data(self) -> Union[Dict[int, Dict[str, Any]], Dict[int, TopLosersData]]:
        """Scrape the CryptoCurrencies which are the top losers in the
        last 24 hours.

        Returns:
            Union[Dict[int, Dict[str, Any]], Dict[int, TopLosersData]]: Scraped data of top losing CryptoCurrencies.
        """
        top_losers: Dict[int, Any] = {}
        page_data = self.__get_page_data
        data = page_data.find_all("tr")
        for num, content in enumerate(data):
            td = content.find_all("td")
            name: str = td[1].find("p", class_="sc-1eb5slv-0 iworPT").text
            symbol: str = (
                td[1].find("p", class_="sc-1eb5slv-0 gGIpIK coin-item-symbol").text
            )
            rank: str = td[0].find("p", class_="sc-1eb5slv-0 bSDVZJ").text
            cmc_link: str = td[1].find("a", class_="cmc-link")["href"]
            price: str = td[2].span.text
            percentage: str = td[3].find("span", class_="sc-15yy2pl-0 hzgCfk").text
            volume_24h: str = td[4].text
            result = {
                "name": name,
                "symbol": symbol,
                "rank": rank,
                "cmc_name": cmc_link.split("/")[-2],
                "url": self.cmc_url + cmc_link,
                "price": price,
                "percentage": percentage,
                "volume_24h": volume_24h,
                "timestamp": datetime.now(),
            }
            if self.out:
                top_losers[num + 1] = result
            else:
                top_losers[num + 1] = TopLosersData(**result)
        return top_losers
