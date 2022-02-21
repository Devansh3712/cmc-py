# type: ignore

import random
import time
from cmc import UpcomingSale


def test_get_data_dict() -> None:
    result = UpcomingSale(as_dict=True).get_data
    time.sleep(2)
    index = random.randint(1, len(result[1]))
    assert len(result) == 1
    assert len(result[1]) == 20
    assert len(result[1][index]) == 10


def test_get_data_model() -> None:
    result = UpcomingSale().get_data
    time.sleep(2)
    index = random.randint(1, len(result[1]))
    assert len(result) == 1
    assert len(result[1]) == 20
    assert len(result[1][index].dict()) == 10
