#!/usr/bin/env python

"""Module for fetching NFT collection rankings from CoinMarketCap website."""

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
from cmc.utils.models import OngoingAirdropsData, UpcomingAirdropsData


class UpcomingAirdrops(CMCBaseClass):
    """Class for scraping the data of the upcoming airdrops."""

    def __init__(self, proxy: Optional[str] = None, as_dict: bool = False) -> None:
        super().__init__(proxy)
        self.base_url = "https://coinmarketcap.com/airdrop/upcoming/"
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
                '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[2]/div/div/table/tbody',
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
    ) -> Union[Dict[int, Dict[str, Any]], Dict[int, UpcomingAirdropsData]]:
        """Scrape the upcoming CryptoCurrency/NFT airdrops.

        Returns:
            Union[Dict[int, Dict[str, Any]], Dict[int, UpcomingAirdropsData]]: Scraped data of trending CryptoCurrencies.
        """
        upcoming: Dict[int, Any] = {}
        page_data = self.__get_page_data
        data = page_data.find_all("tr")
        for num, content in enumerate(data):
            td = content.find_all("td")
            name: str = td[0].find("span", class_="sc-1eb5slv-0 iworPT").text
            symbol: str = td[0].find("span", class_="sc-1eb5slv-0 bkSSMD").text
            cmc_link: str = td[0].find("a", class_="sc-1sea04z-0 jHeqtH cmc-link")[
                "href"
            ]
            winners: str = td[1].text
            airdrop_amount: str = td[2].text
            starts_on: str = td[3].find("div", style="line-height:1").text
            result = {
                "name": name,
                "symbol": symbol,
                "url": self.cmc_url + cmc_link,
                "winners": winners,
                "airdrop_amount": airdrop_amount,
                "starts_on": starts_on,
            }
            if self.out:
                upcoming[num + 1] = result
            else:
                upcoming[num + 1] = UpcomingAirdropsData(**result)
        return upcoming


class OngoingAirdrops(CMCBaseClass):
    """Class for scraping the data of the ongoing airdrops."""

    def __init__(self, proxy: Optional[str] = None, as_dict: bool = False) -> None:
        super().__init__(proxy)
        self.base_url = "https://coinmarketcap.com/airdrop/ongoing/"
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
                '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[2]/div/div/table/tbody',
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
    ) -> Union[Dict[int, Dict[str, Any]], Dict[int, OngoingAirdropsData]]:
        """Scrape the ongoing CryptoCurrency/NFT airdrops.

        Returns:
            Union[Dict[int, Dict[str, Any]], Dict[int, OngoingAirdropsData]]: Scraped data of trending CryptoCurrencies.
        """
        ongoing: Dict[int, Any] = {}
        page_data = self.__get_page_data
        data = page_data.find_all("tr")
        for num, content in enumerate(data):
            td = content.find_all("td")
            name: str = td[0].find("span", class_="sc-1eb5slv-0 iworPT").text
            symbol: str = td[0].find("span", class_="sc-1eb5slv-0 bkSSMD").text
            cmc_link: str = td[0].find("a", class_="sc-1sea04z-0 jHeqtH cmc-link")[
                "href"
            ]
            participated: str = td[1].text
            winners: str = td[2].text
            airdrop_amount: str = td[3].text
            ends_on: str = td[4].find("div", style="line-height:1").text
            result = {
                "name": name,
                "symbol": symbol,
                "url": self.cmc_url + cmc_link,
                "participated": participated,
                "winners": winners,
                "airdrop_amount": airdrop_amount,
                "ends_on": ends_on,
            }
            if self.out:
                ongoing[num + 1] = result
            else:
                ongoing[num + 1] = OngoingAirdropsData(**result)
        return ongoing
