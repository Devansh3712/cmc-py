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
from cmc.utils.models import NFTRankingData


class NFTRanking(CMCBaseClass):
    """Class for scraping NFT collection rankings. Each page
    contains <= 100 NFT collections.
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
        self.base_url = "https://coinmarketcap.com/nft/collections/?page="
        self.ratelimit = ratelimit
        self.pages = pages
        self.out = as_dict

    @property
    def get_data(
        self,
    ) -> Union[
        Dict[int, Dict[int, Dict[str, Any]]], Dict[int, Dict[int, NFTRankingData]]
    ]:
        """Get a dictionary of NFT collection ranks with page number as keys
        and rankings as values.

        Returns:
            Union[Dict[int, Dict[int, Dict[str, Any]]], Dict[int, Dict[int, NFTRankingData]]]: NFT collection rankings of all pages.
        """
        ranks: Dict[int, Dict[int, Any]] = {}
        for page in self.pages:
            start_rank = (page - 1) * 100
            page_data = self.__get_page_data(page)
            ranks[page] = self.__get_nft_ranks(page_data, start_rank)
            start_rank += len(ranks[page])
            time.sleep(self.ratelimit)
        return ranks

    def __get_page_data(self, page: int) -> bs4.BeautifulSoup:
        """Scrape a single ranking page from CoinMarketCap.
        Uses selenium to load javascript elements of the website.

        Args:
            page (int): Page to scrape.

        Raises:
            ScrapeError: Raised when data cannot be scraped from the webpage.

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
                '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[3]/table/tbody',
            )
            page_data = result.get_attribute("innerHTML")
            driver.quit()
            soup = BeautifulSoup(page_data, features="lxml")
            return soup
        except:
            raise ScrapeError

    def __get_nft_ranks(
        self, page_data: bs4.element.Tag, start_rank: int
    ) -> Union[Dict[int, Dict[str, Any]], Dict[int, NFTRankingData]]:
        """Scrape cryptocurrency names and ranks from data returned by
        the __get_page_data() method.

        Args:
            page_data (bs4.element.Tag): Scraped page data.
            start_rank (int): Rank to start storing from.

        Returns:
            Union[Dict[int, Dict[str, Any]], Dict[int, NFTRankingData]]: NFT collection rankings of the current page.
        """
        nft_ranking: Dict[int, Any] = {}
        data = page_data.find_all("tr")
        for rank, content in enumerate(data):
            td = content.find_all("td")
            try:
                name: str = td[2].find_all("span")[1].text
            except:
                name: str = td[1].find("span").text  # type: ignore
            result = {
                "name": name,
                "timestamp": datetime.now(),
            }
            if self.out:
                nft_ranking[start_rank + rank + 1] = result
            else:
                nft_ranking[start_rank + rank + 1] = NFTRankingData(**result)
        return nft_ranking
