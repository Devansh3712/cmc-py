#!/usr/bin/env python

"""Module for fetching CryptoCurrency price predictions made by users
from CoinMarketCap website."""

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
from cmc.utils.models import PricePredictionData


class PricePrediction(CMCBaseClass):
    """Class for scraping cryptocurrency with highest price prediction.
    Each page contains <= 10 cryptocurrencies.
    """

    def __init__(
        self,
        pages: List[int] = [1],
        ratelimit: int = 2,
        proxy: Optional[str] = None,
        as_dict: bool = False,
    ):
        """
        Args:
            pages (List[int], optional): Pages to scrape data from. Defaults to [1].
            ratelimit (int, optional): Ratelimit for parsing each page. Defaults to 2 seconds.
            proxy (Optional[str], optional): Proxy to be used for Selenium and requests Session. Defaults to None.
            as_dict (bool): Return the data as a dictionary. Defaults to False.
        """
        super().__init__(proxy)
        self.base_url = "https://coinmarketcap.com/price-estimates/overview/?page="
        self.ratelimit = ratelimit
        self.pages = pages
        self.out = as_dict

    @property
    def get_data(
        self,
    ) -> Union[
        Dict[int, Dict[int, Dict[str, Any]]], Dict[int, Dict[int, PricePredictionData]]
    ]:
        """Get a dictionary of cryptocurrency ranks with page number as keys
        and price prediction as values.

        Returns:
            Union[Dict[int, Dict[int, Dict[str, Any]]], Dict[int, Dict[int, PricePredictionData]]]: Cryptocurrency rankings of all pages.
        """
        estimates: Dict[int, Dict[int, Any]] = {}
        for page in self.pages:
            start_rank: int = (page - 1) * 10
            page_data = self.__get_page_data(page)
            estimates[page] = self.__get_cryptocurrency_estimates(page_data, start_rank)
            start_rank += len(estimates[page])
            time.sleep(self.ratelimit)
        return estimates

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
                '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody',
            )
            page_data = result.get_attribute("innerHTML")
            driver.quit()
            soup = BeautifulSoup(page_data, features="lxml")
            return soup
        except:
            raise ScrapeError

    def __get_cryptocurrency_estimates(
        self, page_data: bs4.element.Tag, start_rank: int
    ) -> Union[Dict[int, Dict[str, Any]], Dict[int, PricePredictionData]]:
        """Scrape cryptocurrency names and predictions from data returned by
        the __get_page_data() method.

        Args:
            page_data (bs4.element.Tag): Scraped page data.
            start_rank (int): Rank to start storing from.

        Returns:
            Union[Dict[int, Dict[str, Any]], Dict[int, PricePredictionData]]: Cryptocurrency rankings of the current page.
        """
        cryptocurrency_estimates: Dict[int, Any] = {}
        data = page_data.find_all("tr")
        for rank, content in enumerate(data):
            td = content.find_all("td")
            name: str = td[1].find("p", class_="sc-1eb5slv-0 iworPT").text
            symbol: str = (
                td[1].find("p", class_="sc-1eb5slv-0 gGIpIK coin-item-symbol").text
            )
            cmc_link: str = td[1].find("a", class_="cmc-link")["href"]
            accuracy: str = td[2].span.text
            price_date: str = td[3].p.text
            price: str = td[3].text.split(price_date)[0]
            estimation_median: str = td[4].text
            estimation_average: str = td[5].text
            total_estimates: str = td[6].text
            result = {
                "name": name,
                "symbol": symbol,
                "cmc_name": cmc_link.split("/")[-2],
                "url": self.cmc_url + cmc_link,
                "accuracy": accuracy,
                "price": price,
                "price_date": price_date,
                "estimation_median": estimation_median,
                "estimation_average": estimation_average,
                "total_estimate": total_estimates,
                "timestamp": datetime.now(),
            }
            if self.out:
                cryptocurrency_estimates[start_rank + rank + 1] = result
            else:
                cryptocurrency_estimates[start_rank + rank + 1] = PricePredictionData(
                    **result
                )
        return cryptocurrency_estimates
