from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")
    result = response.json()
    assert response.status_code == 200
    assert result["message"] == "CoinMarketCap Unofficial API is working."
    assert result["source_code"] == "https://github.com/Devansh3712/cmc-py"
