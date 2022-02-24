# type: ignore

import random
import time
from cmc import OngoingAirdrops, UpcomingAirdrops


def test_ongoing_airdrops_dict() -> None:
    result = OngoingAirdrops(as_dict=True).get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[index]) == 7


def test_ongoing_airdrops_model() -> None:
    result = OngoingAirdrops().get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[index].dict()) == 7


def test_upcoming_airdrops_dict() -> None:
    result = UpcomingAirdrops(as_dict=True).get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[index]) == 6


def test_upcoming_airdrops_model() -> None:
    result = UpcomingAirdrops().get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[index].dict()) == 6
