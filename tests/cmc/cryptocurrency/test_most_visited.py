import random
import time
from cmc import MostVisited


def test_get_data() -> None:
    result = MostVisited().get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result) == 30
    assert len(result[index]) == 11
