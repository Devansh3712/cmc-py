#!/usr/bin/env python

"""Module for py-cmc methods as API functions."""

from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import cryptocurrency

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(cryptocurrency.router)


@app.get("/")
async def root():
    return {
        "message": "CoinMarketCap Unofficial API is working.",
        "source_code": "https://github.com/Devansh3712/py-cmc",
        "timestamp": datetime.now(),
    }
