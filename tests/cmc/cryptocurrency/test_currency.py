# type: ignore

import time
from typing import Dict, List, Tuple
import pytest
from cmc import CryptoCurrency, CryptoCurrencyData

test_data: List[Tuple[str, Dict[str, str]]] = [
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
]


@pytest.mark.parametrize("cryptocurrency, data", test_data)
def test_get_data_dict(cryptocurrency: str, data: Dict[str, str]) -> None:
    result = CryptoCurrency(cryptocurrency, as_dict=True).get_data
    time.sleep(2)
    assert type(result) == dict
    assert len(result) == 18
    assert result["name"] == data["name"]
    assert result["symbol"] == data["symbol"]
    assert result["max_supply"] == data["max_supply"]
    assert result["cmc_url"] == data["url"]


@pytest.mark.parametrize("cryptocurrency, data", test_data)
def test_get_data_model(cryptocurrency: str, data: Dict[str, str]) -> None:
    result = CryptoCurrency(cryptocurrency).get_data
    time.sleep(2)
    assert type(result) == CryptoCurrencyData
    assert len(result.dict()) == 18
    assert result.name == data["name"]
    assert result.symbol == data["symbol"]
    assert result.max_supply == data["max_supply"]
    assert result.cmc_url == data["url"]


@pytest.mark.parametrize("cryptocurrency", ["btcoin", "etereum"])
def test_invalid_url_exception(cryptocurrency: str) -> None:
    with pytest.raises(Exception) as error:
        time.sleep(2)
        result = CryptoCurrency(cryptocurrency).get_data
