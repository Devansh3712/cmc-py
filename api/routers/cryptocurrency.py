#!/usr/bin/env python

"""Router for cryptocurrency module methods of cmc-py."""

from typing import Dict, List
from fastapi import APIRouter, HTTPException, status, Query
from cmc import (
    CryptoCurrency,
    MostVisited,
    Ranking,
    RecentlyAdded,
    TopGainers,
    TopLosers,
    Trending,
    InvalidCryptoCurrencyURL,
    InvalidPageURL,
)
from api.utils.database import Database
from api.utils.schemas import (
    CryptoCurrencyData,
    MostVisitedData,
    TopGainersData,
    TopLosersData,
    TrendingData,
    RankingData,
    RecentlyAddedData,
)

redis = Database()
router = APIRouter(prefix="/crypto", tags=["CryptoCurrency"])


@router.get("/", response_model=CryptoCurrencyData)
async def cryptocurrency(name: str):
    try:
        if redis.check_data(name):
            return redis.get_data(name)
        result = CryptoCurrency(name, as_dict=True).get_data
        redis.add_data(name, result)  # type: ignore
        return result
    except InvalidCryptoCurrencyURL as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.get("/mostvisited", response_model=Dict[int, MostVisitedData])
async def most_visited():
    try:
        if redis.check_data("mostvisited"):
            return redis.get_data("mostvisited")
        result = MostVisited(as_dict=True).get_data
        redis.add_data("mostvisited", result)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )


@router.get("/topgainers", response_model=Dict[int, TopGainersData])
async def top_gainers():
    try:
        if redis.check_data("topgainers"):
            return redis.get_data("topgainers")
        result = TopGainers(as_dict=True).get_data
        redis.add_data("topgainers", result)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )


@router.get("/toplosers", response_model=Dict[int, TopLosersData])
async def top_losers():
    try:
        if redis.check_data("toplosers"):
            return redis.get_data("toplosers")
        result = TopLosers(as_dict=True).get_data
        redis.add_data("toplosers", result)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )


@router.get("/trending", response_model=Dict[int, TrendingData])
async def trending():
    try:
        if redis.check_data("trending"):
            return redis.get_data("trending")
        result = Trending(as_dict=True).get_data
        redis.add_data("trending", result)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )


@router.get("/ranking", response_model=Dict[int, Dict[int, RankingData]])
async def ranking(pages: List[int] = Query([1])):
    try:
        result = Ranking(pages=pages, as_dict=True).get_data
        return result
    except InvalidPageURL as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.get("/recentlyadded", response_model=Dict[int, RecentlyAddedData])
async def recently_added():
    try:
        if redis.check_data("recentlyadded"):
            return redis.get_data("recentlyadded")
        result = RecentlyAdded(as_dict=True).get_data
        redis.add_data("recentlyadded", result)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )
