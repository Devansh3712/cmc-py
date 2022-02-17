from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "CoinMarketCap Unofficial API is working.",
        "source_code": "https://github.com/Devansh3712/py-cmc",
        "timestamp": datetime.now(),
    }
