#!/usr/bin/env python

"""Router for exchange module methods of py-cmc."""

from typing import Dict
from fastapi import APIRouter, HTTPException, status
from cmc import Derivatives, Dex, Exchange, Lending, Spot, InvalidExchangeURL
from api.schemas import ExchangeData, DerivativesData, DexData, LendingData, SpotData

router = APIRouter(prefix="/exchange", tags=["Exchange"])


@router.get("/", response_model=ExchangeData)
async def exchange(name: str):
    try:
        result = Exchange(name).get_data
        return result
    except InvalidExchangeURL as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.get("/derivatives", response_model=Dict[int, DerivativesData])
async def derivatives():
    try:
        result = Derivatives().get_data
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )


@router.get("/dex", response_model=Dict[int, DexData])
async def dex():
    try:
        result = Dex().get_data
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )


@router.get("/lending", response_model=Dict[int, LendingData])
async def lending():
    try:
        result = Lending().get_data
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )


@router.get("/spot", response_model=Dict[int, SpotData])
async def spot():
    try:
        result = Spot().get_data
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unable to fetch data."
        )
