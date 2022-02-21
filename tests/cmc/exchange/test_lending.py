# type: ignore

import random
import time
from cmc import Lending


def test_get_data_dict() -> None:
    result = Lending(as_dict=True).get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[index]) == 5


def test_get_data_model() -> None:
    result = Lending().get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[index].dict()) == 5
