#!/usr/bin/env python

"""Module for storing settings for Selenium and requests used by
other cmc-py modules.

A random User-Agent and a proxy is used for requests session and Selenium
driver in order to circumvent an IP ban. Data is scraped through Selenium
(to load JavaScript components) and BeautifulSoup (to parse website data).
"""

import os
import random
import re
import time
from typing import Dict, Optional
import requests
from requests.structures import CaseInsensitiveDict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.chrome import ChromeDriverManager
from cmc.resources.user_agents import user_agents
from cmc.utils.exceptions import ProxyTimeOut, InvalidProxy


class CMCBaseClass:
    """Class for basic Selenium and requests settings for cmc-py
    modules. Sets up a random User-Agent and a random proxy each
    time the class is called.
    """

    def __init__(self, proxy: Optional[str]):
        """
        Args:
            proxy (Optional[str]): Proxy to be used for Selenium and requests Session.
        """
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.parent_dir = os.path.dirname(self.current_dir)
        self.cmc_url = "https://coinmarketcap.com"
        self.__proxy_url_1 = "https://public.freeproxyapi.com/api/Proxy/ProxyByType/0/4"
        self.__proxy_url_2 = "http://pubproxy.com/api/proxy?https=true"
        self.headers = CaseInsensitiveDict({"User-Agent": self.__get_random_user_agent})
        self.session = requests.Session()
        self.session.headers = self.headers
        self.proxy: str = self.__get_proxy if proxy is None else proxy
        self.__check_proxy
        self.session.proxies = {"https": self.proxy}
        self.selenium_proxy = Proxy()
        self.selenium_proxy.proxy_type = ProxyType.MANUAL
        self.selenium_proxy.http_proxy = (
            self.selenium_proxy.socks_proxy
        ) = self.selenium_proxy.ssl_proxy = self.proxy
        self.driver_options = webdriver.ChromeOptions()
        self.driver_options.Proxy = self.selenium_proxy
        self.driver_options.add_argument("headless")
        self.driver_options.add_argument("--log-level=3")
        self.driver_options.add_argument("ignore-certificate-errors")
        self.driver_options.add_experimental_option(
            "excludeSwitches", ["enable-logging"]
        )
        self.service = Service(ChromeDriverManager(log_level=0).install())

    @property
    def __get_proxy(self) -> str:
        """Fetch a random HTTPS proxy for using with Selenium.

        Raises:
            ProxyTimeOut: Raised when a proxy cannot be fetched from the API.

        Returns:
            str: Fetched proxy from the API.
        """
        try:
            result = self.session.get(self.__proxy_url_1).json()
            proxy: str = result["host"] + ":" + str(result["port"])
            time.sleep(1.5)
            return proxy
        except:
            try:
                result = self.session.get(self.__proxy_url_2).json()  # type: ignore
                proxy: str = result["data"][0]["ipPort"]  # type: ignore
                time.sleep(1.5)
                return proxy
            except:
                raise ProxyTimeOut

    @property
    def __get_random_user_agent(self) -> str:
        """Fetch a random User-Agent for using with requests
        Session.

        Returns:
            str: User-Agent for requests Session header.
        """
        result: str = random.choice(user_agents)
        return result

    @property
    def __check_proxy(self) -> None:
        """Check whether the proxy (IP:Port) is valid or not.

        Raises:
            InvalidProxy: Raised if the proxy is not valid.
        """
        regex = re.compile(
            r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]+$",
            re.IGNORECASE,
        )
        if not regex.search(self.proxy):
            raise InvalidProxy(self.proxy)
        return
