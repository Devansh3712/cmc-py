#!/usr/bin/env python

"""Module for cmc-py methods as API functions."""

from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import cryptocurrency, exchange, nft

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(cryptocurrency.router)
app.include_router(exchange.router)
app.include_router(nft.router)


@app.get("/")
async def root():
    return {
        "message": "CoinMarketCap Unofficial API is working.",
        "source_code": "https://github.com/Devansh3712/cmc-py",
        "timestamp": datetime.now(),
    }
