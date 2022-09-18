# Third Party
from pytest import raises
from telegram.error import InvalidToken

# First Party
from philapy.messager import Messager


def test_messager_instanciation() -> None:
    """Test that messager instantiate correcly."""
    with raises(InvalidToken):
        Messager(telegram_chat_id="test_chat_id", telegram_token="test_token")
