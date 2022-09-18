"""Helpers modules."""

# Third Party
from yaml import safe_load

# First Party
from philapy.dataclass import AppConfig


def load_config(config_path: str) -> AppConfig:
    """Load config from a file and return AppConfig.

    Args:
        config_path: Path to the config file as str

    Returns:
        AppConfig: An instanciated from file AppConfig instance
    """
    with open(config_path, "r") as f:
        _raw = safe_load(f)
    return AppConfig(
        chrome_path=_raw["chrome_path"],
        refresh_interval=_raw["refresh_interval"],
        redis_url=_raw["redis_url"],
        redis_port=_raw["redis_port"],
    )
