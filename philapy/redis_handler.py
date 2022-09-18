# Standard Library
from dataclasses import asdict
from typing import List

# Third Party
from redis import Redis

# First Party
from philapy.dataclass import Concert


class RedisHandler:
    "RedisHandler class."

    def __init__(self, redis_url: str, redis_port: int) -> None:
        """Init of RedisHandler class.

        Args:
            redis_url: Str representation of the Redis URL
            redis_port: Int representation of the Redis port
        """
        self._r_client = Redis(
            host=redis_url,
            port=redis_port,
            db=0,
            charset="utf-8",
            decode_responses=True,
        )

    def get_concerts_ids(self) -> List[int]:
        """Get all current concert IDs that are in Redis.

        Returns:
            List[int]: A list of int representings IDs
        """
        return [int(id) for id in self._r_client.keys("*")]

    def assert_concert_exists(self, concert_id: int) -> bool:
        """Assert if a concert exists in Redis database.

        Args:
            concert_id: Int representation of a concert ID

        Returns:
            bool: True if concert exists in Redis database
        """
        if self._r_client.exists(f"{concert_id}") != 0:
            return True
        return False

    def append_concert(self, concert: Concert) -> None:
        """Append concert into Redis.

        Args:
            concert: An instanciated ready to be used Concert object
        """
        self._r_client.json().set(f"{concert.id}", "$", asdict(concert))

    def delete_concert(self, concert_id: int) -> None:
        """Delete concert from Redis based on concert_id.

        Args:
            concert_id: Int representation of a concert_id
        """
        self._r_client.delete(f"{concert_id}")
