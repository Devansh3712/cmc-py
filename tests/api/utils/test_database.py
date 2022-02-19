from typing import Dict
import pytest
from api.utils.database import Database

redis = Database()


@pytest.mark.parametrize(
    "name, data",
    [
        ("entry1", {"name": "Devansh", "age": 19}),
        ("entry2", {"name": "Preetika", "age": 18}),
    ],
)
def test_add_data(name: str, data: Dict[str, int]) -> None:
    result = redis.add_data(name, data)
    assert result == True


@pytest.mark.parametrize("name", ("entry1", "entry2"))
def test_check_data(name: str) -> None:
    result = redis.check_data(name)
    assert result == True


@pytest.mark.parametrize(
    "name, data",
    [
        ("entry1", {"name": "Devansh", "age": 19}),
        ("entry2", {"name": "Preetika", "age": 18}),
    ],
)
def test_get_data(name: str, data: Dict[str, int]) -> None:
    result = redis.get_data(name)
    assert result == data


@pytest.mark.parametrize("name", ("entry1", "entry2"))
def test_check_data_exception(name: str) -> None:
    redis.database.delete(name)
    result = redis.check_data(name)
    assert result == False


@pytest.mark.parametrize("name", ("entry1", "entry2"))
def test_get_data_exception(name: str) -> None:
    result = redis.get_data(name)
    assert result == False
