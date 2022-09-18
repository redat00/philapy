"""Dataclasses modules of philapy package."""

# Standard Library
from dataclasses import dataclass


@dataclass
class AppConfig:
    """Dataclass used for configuration of the app."""

    chrome_path: str
    refresh_interval: int
    redis_url: str
    redis_port: int


@dataclass
class Concert:
    id: int
    title: str
    url: str
    date: str
