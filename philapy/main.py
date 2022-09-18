# First Party
from philapy.dataclass import AppConfig
from philapy.messager import Messager
from philapy.redis_handler import RedisHandler
from philapy.scrapper import Scrapper


class Philapy:
    """Philapy class."""

    def __init__(
        self, config: AppConfig, telegram_chat_id: str, telegram_token: str
    ) -> None:
        """Init of Philapy class.

        Args:
            config: An instanciated AppConfig object
            telegram_chat_id: An str representation of telegram chat ID
            telegram_token: An str representation of telegram bot token
        """
        self._rha = RedisHandler(
            redis_url=config.redis_url, redis_port=config.redis_port
        )
        self._scrapper = Scrapper(chrome_path=config.chrome_path)
        self._messager = Messager(
            telegram_chat_id=telegram_chat_id, telegram_token=telegram_token
        )

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
