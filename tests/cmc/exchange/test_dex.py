# type: ignore

import random
import time
from cmc import Dex


def test_get_data_dict() -> None:
    result = Dex(as_dict=True).get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[index]) == 5


def test_get_data_model() -> None:
    result = Dex().get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[index].dict()) == 5
