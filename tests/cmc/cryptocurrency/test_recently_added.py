# type: ignore

import random
import time
from cmc import RecentlyAdded


def test_get_data_dict() -> None:
    result = RecentlyAdded(as_dict=True).get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result) == 30
    assert len(result[index]) == 12


def test_get_data_model() -> None:
    result = RecentlyAdded().get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result) == 30
    assert len(result[index].dict()) == 12
