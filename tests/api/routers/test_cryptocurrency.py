import random
import time
from typing import Dict
from fastapi.testclient import TestClient
import pytest
from api.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "cryptocurrency, data",
    [
        (
            "bitcoin",
            {
                "name": "Bitcoin",
                "symbol": "BTC",
                "max_supply": "21,000,000",
                "url": "https://coinmarketcap.com/currencies/bitcoin",
            },
        ),
        (
            "ethereum",
            {
                "name": "Ethereum",
                "symbol": "ETH",
                "max_supply": "--",
                "url": "https://coinmarketcap.com/currencies/ethereum",
            },
        ),
        (
            "bnb",
            {
                "name": "BNB",
                "symbol": "BNB",
                "max_supply": "165,116,760",
                "url": "https://coinmarketcap.com/currencies/bnb",
            },
        ),
        (
            "xrp",
            {
                "name": "XRP",
                "symbol": "XRP",
                "max_supply": "100,000,000,000",
                "url": "https://coinmarketcap.com/currencies/xrp",
            },
        ),
        (
            "cardano",
            {
                "name": "Cardano",
                "symbol": "ADA",
                "max_supply": "45,000,000,000",
                "url": "https://coinmarketcap.com/currencies/cardano",
            },
        ),
    ],
)
def test_cryptocurrency(cryptocurrency: str, data: Dict[str, str]) -> None:
    response = client.get(f"/crypto/?name={cryptocurrency}")
    result = response.json()
    time.sleep(2)
    assert len(result) == 18
    assert result["name"] == data["name"]
    assert result["symbol"] == data["symbol"]
    assert result["max_supply"] == data["max_supply"]
    assert result["cmc_url"] == data["url"]


@pytest.mark.parametrize("cryptocurrency", ["btcoin", "etereum"])
def test_cryptocurrency_invalid_url_exception(cryptocurrency: str) -> None:
    response = client.get(f"/crypto/?name={cryptocurrency}")
    result = response.json()
    time.sleep(2)
    assert (
        result["detail"]
        == f"https://coinmarketcap.com/currencies/{cryptocurrency} is not a valid webpage."
    )


def test_most_visited() -> None:
    response = client.get(f"/crypto/mostvisited")
    result = response.json()
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result) == 30
    assert len(result[str(index)]) == 11


def test_gainers() -> None:
    response = client.get(f"/crypto/topgainers")
    result = response.json()
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result) == 30
    assert len(result[str(index)]) == 9


def test_losers() -> None:
    response = client.get(f"/crypto/toplosers")
    result = response.json()
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result) == 30
    assert len(result[str(index)]) == 9


def test_trending() -> None:
    response = client.get(f"/crypto/trending")
    result = response.json()
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result) == 30
    assert len(result[str(index)]) == 11


def test_ranking() -> None:
    response = client.get(f"/crypto/ranking")
    result = response.json()
    time.sleep(2)
    index = random.randint(1, len(result["1"]))
    assert len(result) == 1
    assert len(result["1"]) == 100
    assert len(result["1"][str(index)]) == 5


@pytest.mark.parametrize("page", [994675, 34395849])
def test_ranking_invalid_url(page: int) -> None:
    response = client.get(f"/crypto/ranking?pages={page}")
    result = response.json()
    time.sleep(2)
    assert (
        result["detail"]
        == f"https://coinmarketcap.com/?page={page} is not a valid webpage."
    )


def test_recently_added() -> None:
    response = client.get(f"/crypto/recentlyadded")
    result = response.json()
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result) == 30
    assert len(result[str(index)]) == 12
