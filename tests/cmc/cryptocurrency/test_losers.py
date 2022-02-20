# type: ignore

import random
import time
from cmc import TopLosers


def test_get_data_dict() -> None:
    result = TopLosers(as_dict=True).get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result) == 30
    assert len(result[index]) == 9


def test_get_data_model() -> None:
    result = TopLosers().get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result) == 30
    assert len(result[index].dict()) == 9
