import random
import time
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_collection() -> None:
    response = client.get("/nft/ranking")
    result = response.json()
    time.sleep(2)
    index = random.randint(1, len(result["1"]))
    assert len(result) == 1
    assert len(result["1"]) == 100
    assert len(result["1"][str(index)]) == 2


def test_get_data() -> None:
    response = client.get("/nft/upcoming")
    result = response.json()
    time.sleep(2)
    index = random.randint(1, len(result["1"]))
    assert len(result) == 1
    assert len(result["1"]) == 20
    assert len(result["1"][str(index)]) == 10
