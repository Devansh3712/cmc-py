import random
import time
from cmc import Spot


def test_get_data() -> None:
    result = Spot().get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[index]) == 5
