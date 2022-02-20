# type: ignore

import random
import time
from cmc import Trending


def test_get_data_dict() -> None:
    result = Trending(as_dict=True).get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result) == 30
    assert len(result[index]) == 11


def test_get_data_model() -> None:
    result = Trending().get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result) == 30
    assert len(result[index].dict()) == 11
