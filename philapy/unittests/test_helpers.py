# First Party
from philapy.helpers import load_config


def test_load_config() -> None:
    """Test loading a dummy config file."""
    config = load_config("philapy/unittests/dummy_config.yaml")
    assert config.chrome_path == "/snap/bin/chromium.chromedriver"
    assert config.refresh_interval == 60
    assert config.redis_url == "127.0.0.1"
    assert config.redis_port == 6379
