# type: ignore

import random
import time
import pytest
from cmc import Ranking


def test_get_data_dict() -> None:
    result = Ranking(as_dict=True).get_data
    time.sleep(2)
    index = random.randint(1, len(result[1]))
    assert len(result) == 1
    assert len(result[1]) == 100
    assert len(result[1][index]) == 5


def test_get_data_model() -> None:
    result = Ranking().get_data
    time.sleep(2)
    index = random.randint(1, len(result[1]))
    assert len(result) == 1
    assert len(result[1]) == 100
    assert len(result[1][index].dict()) == 5


@pytest.mark.parametrize("page", [994675, 34395849])
def test_invalid_url(page: int) -> None:
    with pytest.raises(Exception) as error:
        result = Ranking([page]).get_data
