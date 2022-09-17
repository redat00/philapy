# Standard Library
from os import getenv
from typing import List

# Third Party
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

# First Party
from philapy.phi_dataclasses import Concert
from philapy.scrapper import Scrapper

NOTES = "🎼"
VIOLIN = "🎻"


def BCOMMAND_START(update: Update, context: CallbackContext):
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


def GET_CURRENT_CONCERT(update: Update, context: CallbackContext):
    """Get current concerts that are a a youth prices.

    Args:
        update: An initiated instance of Update
        context: An initiated instance of CallbackContext
    """
    scrapper = Scrapper()
    concerts = scrapper.get_concerts()
    message = "Here is the list of upcoming concert available at youth price :"
    for concert in concerts:
        message += f"\n{concert.name}\n{concert.url}\n\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


class Messager:
    """Messager class."""

    chat_id = getenv("CHATID_PHILAPY_TELEGRAM")

    def __init__(self) -> None:
        """Init of Messager class."""
        self._updater = Updater(token=getenv("TOKEN_PHILAPY_TELEGRAM"))
        self._dispatcher = self._updater.dispatcher
        start_handler = CommandHandler("start", BCOMMAND_START)
        self._dispatcher.add_handler(start_handler)
        concerts_handler = CommandHandler("get_concerts", GET_CURRENT_CONCERT)
        self._dispatcher.add_handler(concerts_handler)
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
            chat_id=self.chat_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True,
        )
