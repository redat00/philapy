# First Party
from philapy.dataclass import AppConfig, Concert


def test_create_config_dataclass():
    """Test create a AppConfig dataclass."""
    config = AppConfig(
        chrome_path="/usr/bin/chrome",
        refresh_interval=50,
        redis_url="127.0.0.1",
        redis_port=6379,
    )
    assert config.chrome_path == "/usr/bin/chrome"
    assert config.refresh_interval == 50
    assert config.redis_url == "127.0.0.1"
    assert config.redis_port == 6379


def test_create_concert_dataclass():
    """Test create a concert dataclass."""
    concert = Concert(
        id=1, name="A Random Artist Name", url="https://dummy.com"
    )
    assert concert.id == 1
    assert concert.title == "A Random Artist Name"
    assert concert.url == "https://dummy.com"
    assert concert.date is None
