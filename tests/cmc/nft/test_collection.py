# type: ignore

import random
import time
from cmc import NFTRanking


def test_get_data_dict() -> None:
    result = NFTRanking(as_dict=True).get_data
    time.sleep(2)
    index = random.randint(1, len(result[1]))
    assert len(result) == 1
    assert len(result[1]) == 100
    assert len(result[1][index]) == 2


def test_get_data_model() -> None:
    result = NFTRanking().get_data
    time.sleep(2)
    index = random.randint(1, len(result[1]))
    assert len(result) == 1
    assert len(result[1]) == 100
    assert len(result[1][index].dict()) == 2
