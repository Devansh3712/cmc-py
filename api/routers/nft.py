#!/usr/bin/env python

"""Router for NFT module methods of cmc-py."""

from typing import Dict, List
from fastapi import APIRouter, HTTPException, status, Query
from cmc import NFTRanking, UpcomingSale
from api.utils.schemas import NFTRankingData, UpcomingSaleData

router = APIRouter(prefix="/nft", tags=["NFT"])


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
