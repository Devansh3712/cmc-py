import random
import time
from cmc import UpcomingSale


def test_get_data() -> None:
    result = UpcomingSale().get_data
    time.sleep(2)
    index = random.randint(1, len(result[1]))
    assert len(result) == 1
    assert len(result[1]) == 20
    assert len(result[1][index]) == 10
