from api.utils.config import settings


def test_config_validation() -> None:
    assert type(settings.host) == str
    assert type(settings.port) == int
    assert type(settings.expire) == int
