#!/usr/bin/env python

"""Module for creating strawberry schemas for GraphQL responses."""

from datetime import datetime
from typing import Optional, List

import strawberry


@strawberry.type
class CryptoCurrencyData:
    name: str
    symbol: str
    rank: str
    price: str
    price_percent: List[str]
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


@strawberry.type
class MostVisitedData:
    name: str
    symbol: str
    cmc_name: str
    url: str
    price: str
    percent_24h: List[str]
    percent_7d: List[str]
    percent_30d: List[str]
    market_cap: str
    volume_24h: str
    timestamp: datetime


@strawberry.type
class TopGainersData:
    name: str
    symbol: str
    rank: str
    cmc_name: str
    url: str
    price: str
    percentage: str
    volume_24h: str
    timestamp: datetime


@strawberry.type
class TopLosersData:
    name: str
    symbol: str
    rank: str
    cmc_name: str
    url: str
    price: str
    percentage: str
    volume_24h: str
    timestamp: datetime


@strawberry.type
class TrendingData:
    name: str
    symbol: str
    cmc_name: str
    url: str
    price: str
    percent_24h: List[str]
    percent_7d: List[str]
    percent_30d: List[str]
    market_cap: str
    volume_24h: str
    timestamp: datetime


@strawberry.type
class PricePredictionData:
    name: str
    symbol: str
    cmc_name: str
    url: str
    accuracy: str
    price: str
    price_date: str
    estimation_median: str
    estimation_average: str
    total_estimate: str
    timestamp: datetime


@strawberry.type
class RankingData:
    name: str
    symbol: str
    cmc_name: str
    url: str
    timestamp: datetime


@strawberry.type
class RecentlyAddedData:
    name: str
    symbol: str
    cmc_name: str
    url: str
    price: str
    percent_1h: List[str]
    percent_24h: List[str]
    fully_diluted_market_cap: str
    volume_24h: str
    blockchain: str
    added: str
    timestamp: datetime


@strawberry.type
class ExchangeData:
    name: str
    volume_24h: List[str]
    website: str
    cmc_url: str
    timestamp: datetime


@strawberry.type
class DerivativesData:
    name: str
    cmc_link: str
    cmc_name: str
    url: str
    timestamp: datetime


@strawberry.type
class DexData:
    name: str
    cmc_link: str
    cmc_name: str
    url: str
    timestamp: datetime


@strawberry.type
class LendingData:
    name: str
    cmc_link: str
    cmc_name: str
    url: str
    timestamp: datetime


@strawberry.type
class SpotData:
    name: str
    cmc_link: str
    cmc_name: str
    url: str
    timestamp: datetime


@strawberry.type
class NFTRankingData:
    name: str
    timestamp: datetime


@strawberry.type
class OngoingAirdropsData:
    name: str
    symbol: str
    url: str
    participated: str
    winners: str
    airdrop_amount: str
    ends_on: str


@strawberry.type
class UpcomingAirdropsData:
    name: str
    symbol: str
    url: str
    winners: str
    airdrop_amount: str
    starts_on: str


@strawberry.type
class UpcomingSaleData:
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
