# Standard Library
from typing import List

# Third Party
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

# First Party
from philapy.dataclass import Concert

NOTES = "🎼"
VIOLIN = "🎻"


def bcommand_start(update: Update, context: CallbackContext):
    """Start command of the bot.

    Args:
        update: An initiated instance of Update
        context: An initiated instance of CallbackContext
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "Hello there !\n"
            "I'm Philapy, a small bot that will help you find places "
            "at a youth price for “ La Philarmonie de Paris ” 🎼"
        ),
    )


class Messager:
    """Messager class."""

    def __init__(self, telegram_chat_id: str, telegram_token: str) -> None:
        """Init of Messager class."""
        self._chat_id = telegram_chat_id
        self._updater = Updater(token=telegram_token)
        self._dispatcher = self._updater.dispatcher
        start_handler = CommandHandler("start", bcommand_start)
        self._dispatcher.add_handler(start_handler)
        self._updater.start_polling()

    def send_concerts_alerts(self, concert_list: List[Concert]) -> None:
        """Send alert with concerts.

        Args:
            concert_list: List of concert to be send
        """
        if concert_list:
            message = "New concerts are available at a youth price !\n\n"
            for concert in concert_list:
                message += (
                    f"[{concert.title}]({concert.url}) - {concert.date}\n\n"
                )
            message += "I'll let you know if something else shows up !"
            self._send_message(message)

    def _send_message(self, message: str) -> None:
        """Send a message to a channel."""
        self._updater.bot.send_message(
            chat_id=self._chat_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True,
        )
