# type: ignore

import random
import time
from cmc import PricePrediction


def test_get_data_dict() -> None:
    result = PricePrediction(as_dict=True).get_data
    time.sleep(2)
    index = random.randint(1, len(result[1]))
    assert len(result) == 1
    assert len(result[1]) == 10
    assert len(result[1][index]) == 11


def test_get_data_model() -> None:
    result = PricePrediction().get_data
    time.sleep(2)
    index = random.randint(1, len(result[1]))
    assert len(result) == 1
    assert len(result[1]) == 10
    assert len(result[1][index].dict()) == 11
