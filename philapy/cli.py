# Standard Library
from time import sleep

# Third Party
from click import command, option

# First Party
from philapy.helpers import load_config
from philapy.main import Philapy


@command
@option(
    "-c",
    "--config-file",
    help="Path of the configuration file of the application",
    required=True,
)
@option(
    "--telegram-chat-id",
    help="ID of the chat to send alerts to",
    envvar="PHILAPY_TELEGRAM_CHAT_ID",
)
@option(
    "--telegram-token",
    help="Telegram token of the bot",
    envvar="PHILAPY_TELEGRAM_TOKEN",
)
def main(config_file: str, telegram_chat_id: str, telegram_token: str) -> None:
    """Main command to run the app.

    Args:
        config_file_path: Path of the config file as str
        telegram_chat_id: Telegram chat ID as str
        telegram_token: Telegram bot token as str
    """
    config = load_config(config_file)
    while True:
        philapy = Philapy(
            config=config,
            telegram_chat_id=telegram_chat_id,
            telegram_token=telegram_token,
        )
        philapy.fetch()
        sleep(config.refresh_interval)
