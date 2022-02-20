#!/usr/bin/env python

"""Module for storing custom exceptions for cmc-py modules."""


class InvalidPageURL(Exception):
    """Raised when the webpage is not found on CoinMarketCap website."""

    def __init__(self, url: str) -> None:
        """
        Args:
            url (str): Link of the webpage.
        """
        self.url = url

    def __str__(self) -> str:
        return f"{self.url} is not a valid webpage."


class InvalidCryptoCurrencyURL(Exception):
    """Raised when the cryptocurrency webpage is not found on
    CoinMarketCap website."""

    def __init__(self, cryptocurrency: str) -> None:
        """
        Args:
            cryptocurrency (str): Link of the cryptocurrency webpage.
        """
        self.cryptocurrency = cryptocurrency

    def __str__(self) -> str:
        return f"{self.cryptocurrency} is not a valid webpage."


class InvalidExchangeURL(Exception):
    """Raised when the exchange webpage is not found on
    CoinMarketCap website."""

    def __init__(self, exchange: str) -> None:
        """
        Args:
            exchange (str): Link of the exchange webpage.
        """
        self.exchange = exchange

    def __str__(self) -> str:
        return f"{self.exchange} is not a valid webpage."


class ProxyTimeOut(Exception):
    """Raised when a proxy cannot be fetched from the API."""

    def __str__(self) -> str:
        return (
            "A proxy could not be fetched from the API, try again after a few seconds."
        )


class InvalidProxy(Exception):
    """Raised when the proxy used is not valid."""

    def __init__(self, proxy: str) -> None:
        """
        Args:
            proxy (str): The invalid proxy.
        """
        self.proxy = proxy

    def __str__(self) -> str:
        return f"{self.proxy} is not a valid proxy. The proxies should be in the format IP:Port."


class ScrapeError(Exception):
    """Raised when Selenium is unable to scrape required element from the webpage."""

    def __str__(self):
        return "Unable to scrape data from https://coinmarketcap.com/"
