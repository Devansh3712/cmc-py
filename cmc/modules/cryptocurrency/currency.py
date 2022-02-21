#!/usr/bin/env python

"""Module for fetching CryptoCurrency data from CoinMarketCap website."""

from datetime import datetime
import os
import time
from typing import Any, Dict, List, Optional, Tuple, Union
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from cmc.modules.base import CMCBaseClass
from cmc.utils.exceptions import InvalidCryptoCurrencyURL, ScrapeError
from cmc.utils.models import CryptoCurrencyData


class CryptoCurrency(CMCBaseClass):
    """Class for scraping all data of a given CryptoCurrency."""

    def __init__(
        self, cryptocurrency: str, proxy: Optional[str] = None, as_dict: bool = False
    ) -> None:
        """
        Args:
            cryptocurrency (str): Name of Cryptocurrency.
            proxy (Optional[str], optional): Proxy to be used for Selenium and requests Session. Defaults to None.
            as_dict (bool): Return the data as a dictionary. Defaults to False.
        """
        super().__init__(proxy)
        self.base_url = "https://coinmarketcap.com/currencies/"
        self.cryptocurrency = self.base_url + cryptocurrency
        self.out = as_dict

    @property
    def __get_page_data(self) -> bs4.BeautifulSoup:
        """Scrape the CryptoCurrency page data (if it exists) and
        return the scraped data.

        Raises:
            ScrapeError: Raised when data cannot be scraped from the webpage.
            InvalidCryptoCurrencyURL: Raised when the URL is not valid.

        Returns:
            bs4.BeautifulSoup: Scraped page data.
        """
        driver = webdriver.Chrome(
            service=self.service,
            options=self.driver_options,
            service_log_path=os.devnull,
        )
        try:
            driver.get(self.cryptocurrency)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            page_data = driver.page_source
            driver.quit()
        except:
            raise ScrapeError
        if not self.__check_cryptocurrency_url(page_data):
            raise InvalidCryptoCurrencyURL(self.cryptocurrency)
        soup = BeautifulSoup(page_data, features="lxml")
        return soup

    @property
    def get_data(self) -> Union[Dict[str, Any], CryptoCurrencyData]:
        """Scrape the data of a specific CryptoCurrency.

        Returns:
            Union[Dict[str, Any], CryptoCurrencyData]: Scraped CryptoCurrency data.
        """
        page_data = self.__get_page_data
        name: str = (
            str(page_data.find("div", class_="sc-16r8icm-0 gpRPnR nameHeader").h2)
            .split(">", 1)[-1]
            .split("<", 1)[0]
        )
        symbol: str = page_data.find(
            "div", class_="sc-16r8icm-0 gpRPnR nameHeader"
        ).small.text
        rank: str = page_data.find("div", class_="namePill namePillPrimary").text.split(
            "#"
        )[-1]
        price: str = page_data.find("div", class_="priceValue").span.text
        try:
            if page_data.find("span", class_="sc-15yy2pl-0 feeyND").span["class"][0]:
                price_percent: Tuple[str, ...] = (
                    "down",
                    page_data.find("span", class_="sc-15yy2pl-0 feeyND").text,
                )
        except:
            price_percent: Tuple[str, ...] = (  # type: ignore
                "up",
                page_data.find("span", class_="sc-15yy2pl-0 gEePkg").text,
            )
        low: str = (
            page_data.find("div", class_="sc-16r8icm-0 lipEFG")
            .find("span", class_="n78udj-5 dBJPYV")
            .span.text
        )
        high: str = (
            page_data.find("div", class_="sc-16r8icm-0 SjVBR")
            .find("span", class_="n78udj-5 dBJPYV")
            .span.text
        )
        market_cap: str = (
            page_data.find("div", class_="sc-16r8icm-0 fggtJu statsSection")
            .find_all("div", class_="statsItemRight")[0]
            .div.text
        )
        fully_diluted_market_cap: str = (
            page_data.find("div", class_="sc-16r8icm-0 fggtJu statsSection")
            .find_all("div", class_="statsItemRight")[1]
            .div.text
        )
        volume_24h: str = (
            page_data.find("div", class_="sc-16r8icm-0 fggtJu statsSection")
            .find_all("div", class_="statsItemRight")[2]
            .div.text
        )
        volume_by_market_cap: str = (
            page_data.find("div", class_="sc-16r8icm-0 fggtJu statsSection")
            .find_all("div", class_="statsItemRight")[3]
            .div.text
        )
        circulating_supply: str = (
            page_data.find("div", class_="sc-16r8icm-0 inUVOz")
            .find("div", class_="statsValue")
            .text
        )
        circulating_supply_percent: str = (
            page_data.find("div", class_="sc-16r8icm-0 inUVOz")
            .find("div", class_="supplyBlockPercentage")
            .text
        )
        try:
            max_supply: Optional[str] = (
                page_data.find("div", class_="sc-16r8icm-0 dwCYJB")
                .find("div", class_="maxSupplyValue")
                .text
            )
        except:
            max_supply: Optional[str] = None  # type: ignore
        try:
            total_supply: Optional[str] = (
                page_data.find("div", class_="sc-16r8icm-0 hWTiuI")
                .find("div", class_="maxSupplyValue")
                .text
            )
        except:
            total_supply: Optional[str] = None  # type: ignore
        price_change: str = (
            page_data.find("div", class_="sc-16r8icm-0 fmPyWa")
            .tbody.find_all("tr")[1]
            .td.span.text
        )
        cryptocurrency_data: Dict[str, Any] = {
            "name": name,
            "symbol": symbol,
            "rank": rank,
            "price": price,
            "price_percent": price_percent,
            "price_change": price_change,
            "low_24h": low,
            "high_24h": high,
            "market_cap": market_cap,
            "fully_diluted_market_cap": fully_diluted_market_cap,
            "volume_24h": volume_24h,
            "volume_by_market_cap": volume_by_market_cap,
            "circulating_supply": circulating_supply,
            "circulating_supply_percent": circulating_supply_percent,
            "max_supply": max_supply,
            "total_supply": total_supply,
            "cmc_url": self.cryptocurrency,
            "timestamp": datetime.now(),
        }
        if self.out:
            return cryptocurrency_data
        result = CryptoCurrencyData(**cryptocurrency_data)
        return result

    def __check_cryptocurrency_url(self, page_data: str) -> bool:
        """Check whether a webpage for the CryptoCurrency exists
        or not.

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
