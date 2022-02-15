import random
import time
from cmc import Ranking


def test_get_data() -> None:
    result = Ranking().get_data
    time.sleep(2)
    index = random.randint(1, len(result[1]))
    assert len(result) == 1
    assert len(result[1]) == 100
    assert len(result[1][index]) == 5
