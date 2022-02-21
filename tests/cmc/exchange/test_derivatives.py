# type: ignore

import random
import time
from cmc import Derivatives


def test_get_data_dict() -> None:
    result = Derivatives(as_dict=True).get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[index]) == 5


def test_get_data_model() -> None:
    result = Derivatives().get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[index].dict()) == 5
