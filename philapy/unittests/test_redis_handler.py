# First Party
from philapy.redis_handler import RedisHandler


def test_redis() -> None:
    """Test Redis."""
    RedisHandler(redis_url="127.0.0.1", redis_port=6379)
