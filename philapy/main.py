# Standard Library
from time import sleep

# First Party
from philapy.messager import Messager
from philapy.redis_handler import RedisHandler
from philapy.scrapper import Scrapper


class Philapy:
    """Philapy class."""

    def __init__(self) -> None:
        """Init of Philapy class."""
        self._rha = RedisHandler()
        self._scrapper = Scrapper()
        self._messager = Messager()

    def fetch(self) -> None:
        """Fetch data and dispatch it."""
        concerts = self._scrapper.get_concerts()
        redis_ids = self._rha.get_concerts_ids()
        scrapped_concert_ids = [concert.id for concert in concerts]
        for id in redis_ids:
            if id not in scrapped_concert_ids:
                self._rha.delete_concert(id)
        filtered_concerts = []
        for concert in concerts:
            if not self._rha.assert_concert_exists(concert.id):
                self._rha.append_concert(concert)
                filtered_concerts.append(concert)
        self._messager.send_concerts_alerts(filtered_concerts)


if __name__ == "__main__":
    while True:
        philapy = Philapy()
        philapy.fetch()
        sleep(30)
