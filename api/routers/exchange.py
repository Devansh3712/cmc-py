#!/usr/bin/env python

"""Router for exchange module methods of cmc-py."""

from typing import Dict
from fastapi import APIRouter, HTTPException, status
from cmc import Derivatives, Dex, Exchange, Lending, Spot, InvalidExchangeURL
from api.utils.database import Database
from api.utils.schemas import (
    ExchangeData,
    DerivativesData,
    DexData,
    LendingData,
    SpotData,
)

redis = Database()
router = APIRouter(prefix="/exchange", tags=["Exchange"])


@router.get("/", response_model=ExchangeData)
async def exchange(name: str):
    try:
        if redis.check_data(name):
            return redis.get_data(name)
        result = Exchange(name, as_dict=True).get_data
        redis.add_data(name, result)  # type: ignore
        return result
    except InvalidExchangeURL as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.get("/derivatives", response_model=Dict[int, DerivativesData])
async def derivatives():
    try:
        if redis.check_data("derivatives"):
            return redis.get_data("derivatives")
        result = Derivatives(as_dict=True).get_data
        redis.add_data("derivatives", result)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )


@router.get("/dex", response_model=Dict[int, DexData])
async def dex():
    try:
        if redis.check_data("dex"):
            return redis.get_data("dex")
        result = Dex(as_dict=True).get_data
        redis.add_data("dex", result)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )


@router.get("/lending", response_model=Dict[int, LendingData])
async def lending():
    try:
        if redis.check_data("lending"):
            return redis.get_data("lending")
        result = Lending(as_dict=True).get_data
        redis.add_data("lending", result)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )


@router.get("/spot", response_model=Dict[int, SpotData])
async def spot():
    try:
        if redis.check_data("spot"):
            return redis.get_data("spot")
        result = Spot(as_dict=True).get_data
        redis.add_data("spot", result)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )
