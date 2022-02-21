#!/usr/bin/env python

"""Module for fetching Exchange data from CoinMarketCap website."""

from datetime import datetime
import os
import time
from typing import Any, Dict, List, Optional, Tuple, Union
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from cmc.modules.base import CMCBaseClass
from cmc.utils.exceptions import InvalidExchangeURL
from cmc.utils.models import ExchangeData


class Exchange(CMCBaseClass):
    def __init__(
        self, exchange: str, proxy: Optional[str] = None, as_dict: bool = False
    ) -> None:
        """
        Args:
            exchange (str): Name of the exchange.
            proxy (Optional[str], optional): Proxy to be used for Selenium and requests Session. Defaults to None.
            as_dict (bool): Return the data as a dictionary. Defaults to False.
        """
        super().__init__(proxy)
        self.base_url = "https://coinmarketcap.com/exchanges/"
        self.exchange = self.base_url + exchange
        self.out = as_dict

    @property
    def __get_page_data(self) -> bs4.BeautifulSoup:
        """Scrape the Exchange page data (if it exists) and return
        the scraped data.

        Raises:
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
            driver.get(self.exchange)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            page_data = driver.page_source
            driver.quit()
            if not self.__check_cryptocurrency_url(page_data):
                raise InvalidExchangeURL(self.exchange)
            soup = BeautifulSoup(page_data, features="lxml")
            return soup
        except:
            raise InvalidExchangeURL(self.exchange)

    @property
    def get_data(self) -> Union[Dict[str, Any], ExchangeData]:
        """Scrape the data of a specific Exchange.

        Returns:
            Union[Dict[str, Any], ExchangeData]: Scraped Exchange data.
        """
        page_data = self.__get_page_data
        name: str = page_data.find("h2", class_="sc-1q9q90x-0 sc-1xafy60-3 dzkWnG").text
        volume_24h: Tuple[str, ...] = (
            page_data.find("span", class_="sc-1eb5slv-0 kjqbLV priceText").text,
            page_data.find("p", class_="sc-1eb5slv-0 jsOvhb").text,
        )
        website: str = page_data.find(
            "ul", class_="uxo8xk-0 jlcQeb cmc-details-panel-links"
        ).li.a.text
        exchange_data: Dict[str, Any] = {
            "name": name,
            "volume_24h": volume_24h,
            "website": website,
            "cmc_url": self.exchange,
            "timestamp": datetime.now(),
        }
        if self.out:
            return exchange_data
        result = ExchangeData(**exchange_data)
        return result

    def __check_cryptocurrency_url(self, page_data: str) -> bool:
        """Check whether a webpage for the Exchange exists or not.

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
