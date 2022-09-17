"""Dataclasses modules of philapy package."""

# Standard Library
from dataclasses import dataclass


@dataclass
class Concert:
    id: int
    title: str
    url: str
    date: str
