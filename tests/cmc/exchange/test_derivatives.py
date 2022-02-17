import random
import time
from cmc import Derivatives


def test_get_data() -> None:
    result = Derivatives().get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[index]) == 5
