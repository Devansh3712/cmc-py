#!/usr/bin/env python

"""Module for converting `cmc-py` return values to Pydantic models."""

from datetime import datetime
from typing import Optional, Tuple
from pydantic import BaseModel


class CryptoCurrencyData(BaseModel):
    name: str
    symbol: str
    rank: str
    price: str
    price_percent: Tuple[str, ...]
    price_change: str
    low_24h: str
    high_24h: str
    market_cap: str
    fully_diluted_market_cap: str
    volume_24h: str
    volume_by_market_cap: str
    circulating_supply: str
    circulating_supply_percent: str
    max_supply: Optional[str]
    total_supply: Optional[str]
    cmc_url: str
    timestamp: datetime


class MostVisitedData(BaseModel):
    name: str
    symbol: str
    cmc_name: str
    url: str
    price: str
    percent_24h: Tuple[str, ...]
    percent_7d: Tuple[str, ...]
    percent_30d: Tuple[str, ...]
    market_cap: str
    volume_24h: str
    timestamp: datetime


class TopGainersData(BaseModel):
    name: str
    symbol: str
    rank: str
    cmc_name: str
    url: str
    price: str
    percentage: str
    volume_24h: str
    timestamp: datetime


class TopLosersData(BaseModel):
    name: str
    symbol: str
    rank: str
    cmc_name: str
    url: str
    price: str
    percentage: str
    volume_24h: str
    timestamp: datetime


class TrendingData(BaseModel):
    name: str
    symbol: str
    cmc_name: str
    url: str
    price: str
    percent_24h: Tuple[str, ...]
    percent_7d: Tuple[str, ...]
    percent_30d: Tuple[str, ...]
    market_cap: str
    volume_24h: str
    timestamp: datetime


class RankingData(BaseModel):
    name: str
    symbol: str
    cmc_name: str
    url: str
    timestamp: datetime


class RecentlyAddedData(BaseModel):
    name: str
    symbol: str
    cmc_name: str
    url: str
    price: str
    percent_1h: Tuple[str, ...]
    percent_24h: Tuple[str, ...]
    fully_diluted_market_cap: str
    volume_24h: str
    blockchain: str
    added: str
    timestamp: datetime


class ExchangeData(BaseModel):
    name: str
    volume_24h: Tuple[str, ...]
    website: str
    cmc_url: str
    timestamp: datetime


class DerivativesData(BaseModel):
    name: str
    cmc_link: str
    cmc_name: str
    url: str
    timestamp: datetime


class DexData(BaseModel):
    name: str
    cmc_link: str
    cmc_name: str
    url: str
    timestamp: datetime


class LendingData(BaseModel):
    name: str
    cmc_link: str
    cmc_name: str
    url: str
    timestamp: datetime


class SpotData(BaseModel):
    name: str
    cmc_link: str
    cmc_name: str
    url: str
    timestamp: datetime


class NFTRankingData(BaseModel):
    name: str
    timestamp: datetime


class UpcomingSaleData(BaseModel):
    name: str
    blockchain: str
    info: str
    discord: str
    twitter: str
    website: str
    sale_on: str
    pre_sale: Optional[str]
    sale: str
    timestamp: datetime
