# type: ignore

import time
from typing import Dict, List, Tuple
import pytest
from cmc import Exchange

test_data: List[Tuple[str, Dict[str, str]]] = [
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
]


@pytest.mark.parametrize("exchange, data", test_data)
def test_get_data_dict(exchange: str, data: Dict[str, str]) -> None:
    result = Exchange(exchange, as_dict=True).get_data
    time.sleep(2)
    assert len(result) == 5
    assert result["name"] == data["name"]
    assert result["website"] == data["website"]


@pytest.mark.parametrize("exchange, data", test_data)
def test_get_data_model(exchange: str, data: Dict[str, str]) -> None:
    result = Exchange(exchange).get_data
    time.sleep(2)
    assert len(result.dict()) == 5
    assert result.name == data["name"]
    assert result.website == data["website"]


@pytest.mark.parametrize("exchange", ["biance", "conbase"])
def test_invalid_url_exception(exchange: str) -> None:
    with pytest.raises(Exception) as error:
        result = Exchange(exchange).get_data
