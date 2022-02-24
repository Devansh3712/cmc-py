#!/usr/bin/env python

"""Router for NFT module methods of cmc-py."""

from typing import Dict, List
from fastapi import APIRouter, HTTPException, status, Query
from cmc import NFTRanking, OngoingAirdrops, UpcomingAirdrops, UpcomingSale
from api.utils.database import Database
from api.utils.schemas import (
    NFTRankingData,
    OngoingAirdropsData,
    UpcomingAirdropsData,
    UpcomingSaleData,
)

redis = Database()
router = APIRouter(prefix="/nft", tags=["NFT"])


@router.get("/ongoingairdrops", response_model=Dict[int, OngoingAirdropsData])
async def ongoing_airdrops():
    try:
        if redis.check_data("ongoingairdrops"):
            return redis.get_data("ongoingairdrops")
        result = OngoingAirdrops(as_dict=True).get_data
        redis.add_data("ongoingairdrops", result)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )


@router.get("/ranking", response_model=Dict[int, Dict[int, NFTRankingData]])
async def ranking(pages: List[int] = Query([1])):
    try:
        result = NFTRanking(pages, as_dict=True).get_data
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )


@router.get("/upcoming", response_model=Dict[int, Dict[int, UpcomingSaleData]])
async def upcoming(pages: List[int] = Query([1])):
    try:
        result = UpcomingSale(pages, as_dict=True).get_data
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )


@router.get("/upcomingairdrops", response_model=Dict[int, UpcomingAirdropsData])
async def upcoming_airdrops():
    try:
        if redis.check_data("upcomingairdrops"):
            return redis.get_data("upcomingairdrops")
        result = UpcomingAirdrops(as_dict=True).get_data
        redis.add_data("upcomingairdrops", result)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )
