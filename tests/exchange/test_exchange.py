import time
from typing import Dict
import pytest
from cmc import Exchange


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
def test_get_data(exchange: str, data: Dict[str, str]) -> None:
    result = Exchange(exchange).get_data
    time.sleep(2)
    assert len(result) == 5
    assert result["name"] == data["name"]
    assert result["website"] == data["website"]


@pytest.mark.parametrize("exchange", ["biance", "conbase"])
def test_invalid_url_exception(exchange: str) -> None:
    with pytest.raises(Exception) as error:
        result = Exchange(exchange).get_data
