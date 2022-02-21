#!/usr/bin/env python

"""Module for fetching dex exchange rankings from CoinMarketCap
website."""

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
from cmc.utils.models import DexData


class Dex(CMCBaseClass):
    """Class for scraping the data of top dex exchanges."""

    def __init__(self, proxy: Optional[str] = None, as_dict: bool = False) -> None:
        """
        Args:
            proxy (Optional[str], optional): Proxy to be used for Selenium and requests Session. Defaults to None.
            as_dict (bool): Return the data as a dictionary. Defaults to False.
        """
        super().__init__(proxy)
        self.base_url = "https://coinmarketcap.com/rankings/exchanges/dex/"
        self.out = as_dict

    @property
    def __get_page_data(self) -> bs4.BeautifulSoup:
        """Scrape the table from top dex exchanges page data and return
        the scraped data.

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
    def get_data(self) -> Union[Dict[int, Dict[str, Any]], Dict[int, DexData]]:
        """Scrape exchanges names and ranks from data returned by
        __get_page_data() method.

        Returns:
            Union[Dict[int, Dict[str, Any]], Dict[int, DexData]]: Exchange platform rankings.
        """
        dex: Dict[int, Any] = {}
        page_data = self.__get_page_data
        data = page_data.find_all("tr")
        for rank, content in enumerate(data):
            td = content.find_all("td")[1]
            try:
                name: str = td.find("p", class_="sc-1eb5slv-0 iworPT").text
            except:
                name: str = td.text  # type: ignore
            cmc_link: str = td.find("a", class_="cmc-link")["href"]
            result = {
                "name": name,
                "cmc_link": cmc_link,
                "cmc_name": cmc_link.split("/")[-2],
                "url": self.cmc_url + cmc_link,
                "timestamp": datetime.now(),
            }
            if self.out:
                dex[rank + 1] = result
            else:
                dex[rank + 1] = DexData(**result)
        return dex
