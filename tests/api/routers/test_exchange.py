import random
import time
from typing import Dict
from fastapi.testclient import TestClient
import pytest
from api.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "exchange, data",
    [
        ("binance", {"name": "Binance", "website": "https://www.binance.com/"}),
        (
            "crypto-com-exchange",
            {"name": "Crypto.com Exchange", "website": "https://crypto.com/exchange"},
        ),
        (
            "blockchain-com-exchange",
            {"name": "Blockchain.com", "website": "https://blockchain.com/"},
        ),
        (
            "coinbase-exchange",
            {"name": "Coinbase Exchange", "website": "https://pro.coinbase.com"},
        ),
    ],
)
def test_exchange(exchange: str, data: Dict[str, str]) -> None:
    response = client.get(f"/exchange/?name={exchange}")
    result = response.json()
    time.sleep(2)
    assert len(result) == 5
    assert result["name"] == data["name"]
    assert result["website"] == data["website"]


@pytest.mark.parametrize("exchange", ["biance", "conbase"])
def test_exchange_invalid_url_exception(exchange: str) -> None:
    response = client.get(f"/exchange/?name={exchange}")
    result = response.json()
    time.sleep(2)
    assert (
        result["detail"]
        == f"https://coinmarketcap.com/exchanges/{exchange} is not a valid webpage."
    )


def test_derivatives() -> None:
    response = client.get(f"/exchange/derivatives")
    result = response.json()
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[str(index)]) == 5


def test_dex() -> None:
    response = client.get(f"/exchange/dex")
    result = response.json()
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[str(index)]) == 5


def test_lending() -> None:
    response = client.get(f"/exchange/lending")
    result = response.json()
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[str(index)]) == 5


def test_spot() -> None:
    response = client.get(f"/exchange/spot")
    result = response.json()
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[str(index)]) == 5
