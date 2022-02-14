#!/usr/bin/env python

"""Module for storing custom exceptions for py-cmc modules."""


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

    def __str__(self):
        return f"{self.proxy} is not a valid proxy. The proxies should be in the format IP:Port."
