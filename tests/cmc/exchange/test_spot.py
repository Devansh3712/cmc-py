# type: ignore

import random
import time
from cmc import Spot


def test_get_data_dict() -> None:
    result = Spot(as_dict=True).get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[index]) == 5


def test_get_data_model() -> None:
    result = Spot().get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[index].dict()) == 5
